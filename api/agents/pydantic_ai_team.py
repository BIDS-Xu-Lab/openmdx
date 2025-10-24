"""Clinical Diagnosis Team using Pydantic AI and Graph.

This module implements a multi-agent clinical diagnosis workflow using pydantic-graph,
mirroring the smolagent_team.py workflow with specialized medical agents.

Run with:
    uv run -m api.agents.pydantic_ai_team
"""

from __future__ import annotations as _annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

import logfire
from pydantic import BaseModel

from pydantic_ai import Agent, ModelMessage, format_as_xml
from pydantic_graph import (
    BaseNode,
    End,
    Graph,
    GraphRunContext,
)
from pydantic_graph.persistence.file import FileStatePersistence

from dotenv import load_dotenv

load_dotenv()

# Configure logfire
logfire.configure(send_to_logfire='if-token-present')
logfire.instrument_pydantic_ai()


@dataclass
class ClinicalState:
    """State for the clinical diagnosis workflow."""
    patient_summary: str
    evidence_snippets: List[Dict[str, Any]]
    current_meds: Optional[str] = None
    allergies: Optional[str] = None
    labs: Optional[str] = None
    imaging: Optional[str] = None
    
    # Agent outputs
    multi_specialist_output: Optional[str] = None
    warning_output: Optional[str] = None
    review_output: Optional[str] = None
    verification_output: Optional[str] = None
    reasoning_output: Optional[str] = None
    action_output: Optional[str] = None
    
    # Message histories for each agent
    multi_specialist_messages: List[ModelMessage] = field(default_factory=list)
    warning_messages: List[ModelMessage] = field(default_factory=list)
    review_messages: List[ModelMessage] = field(default_factory=list)
    verification_messages: List[ModelMessage] = field(default_factory=list)
    reasoning_messages: List[ModelMessage] = field(default_factory=list)
    action_messages: List[ModelMessage] = field(default_factory=list)


# Define output models for each agent
class MultiSpecialistOutput(BaseModel):
    differential: str
    """5-10 candidate diagnoses prioritized with rationale and citations."""


class WarningOutput(BaseModel):
    red_flags: List[str]
    """Up to 5 red flags with evidence citations."""
    urgent_actions: List[str]
    """Up to 3 urgent actions with rationale."""


class ReviewOutput(BaseModel):
    merged_differential: str
    """Prioritized differential list merging specialist and warning outputs."""


class VerificationOutput(BaseModel):
    verified_differential: str
    """Cleaned differential with guideline fit assessments."""


class ReasoningOutput(BaseModel):
    detailed_differential: str
    """Detailed diagnostic narrative for each verified diagnosis."""


class ActionOutput(BaseModel):
    treatment_plan: str
    """Treatment and next-step plan with rationale."""


class FinalOutput(BaseModel):
    text: str
    """Final summary of the clinical case analysis."""
    diagnoses: List[Dict[str, Any]]
    """List of diagnoses with details."""
    red_flags: List[str]
    """List of red flags."""
    treatment_plan: Dict[str, List[str]]
    """Treatment plan structure."""
    evidence_list: List[Dict[str, Any]]
    """List of evidence snippets used."""


# Initialize agents
multi_specialist_agent = Agent(
    'openai:gpt-5-nano',
    output_type=MultiSpecialistOutput,
    system_prompt="""You are a panel of board-certified specialists (cardiology, nephrology, endocrinology, infectious disease, geriatrics).
Task: propose a comprehensive *differential diagnosis list* for the current clinical case.

INPUTS
- patient_summary: a summary of the patient's clinical history, including the patient's symptoms, medical history, and medications.
- evidence_snippets: JSON array of evidence objects; each has snippet_id and text.
- current_meds / allergies / labs / imaging if provided.

REQUIRED OUTPUT (markdown bullets):
- 5-10 candidate diagnoses prioritized (highest first).
- For each item:
  - one-line rationale referencing key evidence with <cite>snippet_id</cite>.
  - optional probability (0-1) if you're confident.
  - red flags if applicable.

CONSTRAINTS
- Be precise and concise (≤ 2 lines per diagnosis).
- Only cite from evidence_snippets using <cite>id</cite>.
- No treatment recommendations here.
- stage: "intermediate".
""",
)

warning_agent = Agent(
    'openai:gpt-5-nano',
    output_type=WarningOutput,
    system_prompt="""You detect *immediate dangers* and *can't-miss diagnoses* (red flags) from the same inputs.

OUTPUT
- "red_flags": up to 5 bullets, each a short sentence with evidence <cite>snippet_id</cite>.
- "urgent_actions": up to 3 bullets (diagnostic stabilization ideas, not definitive treatment).

CONSTRAINTS
- Keep it brief. No probabilities.
- Use only evidence_snippets for citations.
- stage: "intermediate".
""",
)

review_agent = Agent(
    'openai:gpt-5-nano',
    output_type=ReviewOutput,
    system_prompt="""You merge (A) the multi-specialist differential and (B) the warning agent red flags.

OUTPUT
- A single prioritized differential list (top 5-8).
- For each diagnosis: one-line rationale with citations <cite>snippet_id</cite>.
- Mark any diagnosis that directly addresses a red flag.

CONSTRAINTS
- Do not add new diagnoses without evidence.
- stage: "intermediate".
""",
)

verification_agent = Agent(
    'openai:gpt-5-nano',
    output_type=VerificationOutput,
    system_prompt="""You verify each diagnosis against contemporary clinical guidelines and major trial evidence *present in evidence_snippets*.

TASK
- For each diagnosis in the review list:
  - "guideline_fit": "fit" | "uncertain" | "not_fit"
  - "notes": one line with citations <cite>snippet_id</cite>.
- Remove items that are "not_fit" unless clearly life-threatening.

OUTPUT
- A cleaned, ordered differential (top 3-6) with guideline_fit and notes.

CONSTRAINTS
- Cite only from evidence_snippets (<cite>id</cite>); if evidence lacking, mark "uncertain".
- stage: "intermediate".
""",
)

reasoning_agent = Agent(
    'openai:gpt-5-nano',
    output_type=ReasoningOutput,
    system_prompt="""You write the *detailed diagnostic narrative* for each verified diagnosis.

FOR EACH DIAGNOSIS (short section):
- "why_this": 2-4 sentences connecting findings → pathophysiology, with citations <cite>snippet_id</cite>.
- "why_not_others": ≤2 short bullets contrasting key alternatives, with citations.
- "evidence_list": 3-6 bullet points: quote short fragments or paraphrase + <cite>id</cite>.

STYLE
- Clear, clinical, concise; no treatment.
- Only cite available evidence_snippets.
- stage: "intermediate".
""",
)

action_agent = Agent(
    'openai:gpt-5-nano',
    output_type=ActionOutput,
    system_prompt="""You propose a concise *treatment & next-step plan* tailored to the verified diagnoses and patient comorbidities.

OUTPUT (structured bullets):
- "initial_management": 3-6 bullets (med changes/starts, monitoring), each with one-line rationale + <cite>id</cite>.
- "diagnostic_workup": 2-4 bullets with expected value (why it changes management) + <cite>id</cite>.
- "safety_checks": potassium/renal/BP/volume status, drug-drug/contraindications (each with citation).
- "follow_up": timing and targets (labs, vitals, symptoms).

CONSTRAINTS
- Respect CKD/age/comorbidity constraints from evidence.
- Keep total length tight but complete.
- stage: "intermediate".
""",
)

manager_agent = Agent(
    'openai:gpt-5-nano',
    output_type=FinalOutput,
    system_prompt="""You orchestrate the full pipeline and return a single JSON as the final result.

GLOBAL INPUTS
- patient_summary: a summary of the patient's clinical history, including the patient's symptoms, medical history, and medications.
- current_meds / allergies / labs / imaging if provided.
- evidence_snippets: optionally, a list of evidence

PIPELINE (strict order)
1) Ask multi_specialist_agent to generate an initial differential.
2) In parallel, ask warning_agent to produce red_flags.
3) Send both to review_agent → get a merged, prioritized differential.
4) Send merged list to verification_agent → drop items marked "not_fit" (unless life-threatening, then keep with "uncertain").
5) Send the cleaned list to reasoning_agent → get detailed explanations and evidence lists.
6) Send the cleaned list to action_agent → get treatment & next steps plan.
7) Synthesize FINAL JSON and return.

FINAL JSON CONTRACT (return exactly this shape):
{
  "text": "the final summary of the clinical case, including the differential diagnosis, the treatment plan, and the next steps in markdown format",
  "diagnoses": [
    {
      "label": "Diagnosis name",
      "priority": 1,
      "probability": 0.0_to_1.0_or_null,
      "guideline_fit": "fit|uncertain",
      "why_this": "2-4 sentences with <cite>id</cite>.",
      "why_not_others": ["short bullet with <cite>id</cite>", "..."],
      "evidence_list": ["short point with <cite>id</cite>", "..."]
    }
  ],
  "red_flags": ["short sentence with <cite>id</cite>", "..."],
  "treatment_plan": {
    "initial_management": ["bullet with rationale + <cite>id</cite>", "..."],
    "diagnostic_workup": ["bullet with expected impact + <cite>id</cite>", "..."],
    "safety_checks": ["bullet + <cite>id</cite>", "..."],
    "follow_up": ["bullet + <cite>id</cite>", "..."]
  },
  "evidence_list": [
    {
        "snippet_id": "the id of the evidence snippet",
        "text": "the text of the evidence snippet",
        "source_id": "the id of the source of the evidence snippet",
        "source_type": "the type of the source of the evidence snippet",
        "source_url": "the url of the source of the evidence snippet",
    }, ...
  ]
}

RENDERING & CITATIONS
- All clinical claims must cite evidence_snippets using <cite>snippet_id</cite>.
- Do NOT invent IDs; only use provided snippet_ids.
- Prefer concise, high-yield sentences.
- Tag your final message with stage: "final".

FAIL-SAFE
- If a required component is missing from upstream agents, degrade gracefully: still return the JSON with best available content and note "uncertain" where needed.
- If inputs conflict, document the conflict briefly in "text" with citations.

Return ONLY the JSON (no extra prose).
""",
)


# Graph nodes following the pydantic-graph pattern
@dataclass
class MultiSpecialistNode(BaseNode[ClinicalState]):
    async def run(self, ctx: GraphRunContext[ClinicalState]) -> WarningNode:
        """Generate initial differential diagnosis."""
        result = await multi_specialist_agent.run(
            format_as_xml({
                'patient_summary': ctx.state.patient_summary,
                'evidence_snippets': ctx.state.evidence_snippets,
                'current_meds': ctx.state.current_meds,
                'allergies': ctx.state.allergies,
                'labs': ctx.state.labs,
                'imaging': ctx.state.imaging,
            }),
            message_history=ctx.state.multi_specialist_messages,
        )
        ctx.state.multi_specialist_messages += result.new_messages()
        ctx.state.multi_specialist_output = result.output.differential
        return WarningNode()


@dataclass
class WarningNode(BaseNode[ClinicalState]):
    async def run(self, ctx: GraphRunContext[ClinicalState]) -> ReviewNode:
        """Detect red flags and urgent actions."""
        result = await warning_agent.run(
            format_as_xml({
                'patient_summary': ctx.state.patient_summary,
                'evidence_snippets': ctx.state.evidence_snippets,
                'current_meds': ctx.state.current_meds,
                'allergies': ctx.state.allergies,
                'labs': ctx.state.labs,
                'imaging': ctx.state.imaging,
            }),
            message_history=ctx.state.warning_messages,
        )
        ctx.state.warning_messages += result.new_messages()
        ctx.state.warning_output = json.dumps({
            'red_flags': result.output.red_flags,
            'urgent_actions': result.output.urgent_actions,
        })
        return ReviewNode()


@dataclass
class ReviewNode(BaseNode[ClinicalState]):
    async def run(self, ctx: GraphRunContext[ClinicalState]) -> VerificationNode:
        """Merge specialist differential and warning outputs."""
        result = await review_agent.run(
            format_as_xml({
                'multi_specialist_output': ctx.state.multi_specialist_output,
                'warning_output': ctx.state.warning_output,
                'patient_summary': ctx.state.patient_summary,
                'evidence_snippets': ctx.state.evidence_snippets,
            }),
            message_history=ctx.state.review_messages,
        )
        ctx.state.review_messages += result.new_messages()
        ctx.state.review_output = result.output.merged_differential
        return VerificationNode()


@dataclass
class VerificationNode(BaseNode[ClinicalState]):
    async def run(self, ctx: GraphRunContext[ClinicalState]) -> ReasoningNode:
        """Verify diagnoses against clinical guidelines."""
        result = await verification_agent.run(
            format_as_xml({
                'review_output': ctx.state.review_output,
                'evidence_snippets': ctx.state.evidence_snippets,
            }),
            message_history=ctx.state.verification_messages,
        )
        ctx.state.verification_messages += result.new_messages()
        ctx.state.verification_output = result.output.verified_differential
        return ReasoningNode()


@dataclass
class ReasoningNode(BaseNode[ClinicalState]):
    async def run(self, ctx: GraphRunContext[ClinicalState]) -> ActionNode:
        """Write detailed diagnostic narrative."""
        result = await reasoning_agent.run(
            format_as_xml({
                'verification_output': ctx.state.verification_output,
                'evidence_snippets': ctx.state.evidence_snippets,
            }),
            message_history=ctx.state.reasoning_messages,
        )
        ctx.state.reasoning_messages += result.new_messages()
        ctx.state.reasoning_output = result.output.detailed_differential
        return ActionNode()


@dataclass
class ActionNode(BaseNode[ClinicalState]):
    async def run(self, ctx: GraphRunContext[ClinicalState]) -> ManagerNode:
        """Generate treatment and next-step plan."""
        result = await action_agent.run(
            format_as_xml({
                'reasoning_output': ctx.state.reasoning_output,
                'patient_summary': ctx.state.patient_summary,
                'evidence_snippets': ctx.state.evidence_snippets,
            }),
            message_history=ctx.state.action_messages,
        )
        ctx.state.action_messages += result.new_messages()
        ctx.state.action_output = result.output.treatment_plan
        return ManagerNode()


@dataclass
class ManagerNode(BaseNode[ClinicalState]):
    async def run(self, ctx: GraphRunContext[ClinicalState]) -> End[FinalOutput]:
        """Synthesize final JSON result."""
        result = await manager_agent.run(
            format_as_xml({
                'patient_summary': ctx.state.patient_summary,
                'evidence_snippets': ctx.state.evidence_snippets,
                'current_meds': ctx.state.current_meds,
                'allergies': ctx.state.allergies,
                'labs': ctx.state.labs,
                'imaging': ctx.state.imaging,
                'multi_specialist_output': ctx.state.multi_specialist_output,
                'warning_output': ctx.state.warning_output,
                'review_output': ctx.state.review_output,
                'verification_output': ctx.state.verification_output,
                'reasoning_output': ctx.state.reasoning_output,
                'action_output': ctx.state.action_output,
            })
        )
        return End(result.output)


# Create the clinical diagnosis graph
clinical_graph = Graph(
    nodes=(MultiSpecialistNode, WarningNode, ReviewNode, VerificationNode, ReasoningNode, ActionNode, ManagerNode),
    state_type=ClinicalState
)


async def run_clinical_diagnosis(patient_summary: str, evidence_snippets: List[Dict[str, Any]] = None, 
                                current_meds: str = None, allergies: str = None, 
                                labs: str = None, imaging: str = None):
    """Run the clinical diagnosis workflow using pydantic-graph."""
    state = ClinicalState(
        patient_summary=patient_summary,
        evidence_snippets=evidence_snippets or [],
        current_meds=current_meds,
        allergies=allergies,
        labs=labs,
        imaging=imaging
    )
    
    node = MultiSpecialistNode()
    result = await clinical_graph.run(node, state=state)
    return result.output


async def run_with_persistence(patient_summary: str, evidence_snippets: List[Dict[str, Any]] = None,
                              current_meds: str = None, allergies: str = None,
                              labs: str = None, imaging: str = None):
    """Run with state persistence for debugging."""
    persistence = FileStatePersistence(Path('clinical_graph.json'))
    persistence.set_graph_types(clinical_graph)
    
    state = ClinicalState(
        patient_summary=patient_summary,
        evidence_snippets=evidence_snippets or [],
        current_meds=current_meds,
        allergies=allergies,
        labs=labs,
        imaging=imaging
    )
    
    node = MultiSpecialistNode()
    
    async with clinical_graph.iter(node, state=state, persistence=persistence) as run:
        while True:
            node = await run.next()
            if isinstance(node, End):
                print('Clinical Diagnosis Complete!')
                print('Result:', node.data)
                history = await persistence.load_all()
                print('Execution History:', '\n'.join(str(e.node) for e in history), sep='\n')
                break
            # Continue to next node
            print(f'Executing: {type(node).__name__}')


if __name__ == '__main__':
    import asyncio
    import sys
    
    # Sample clinical case from smolagent_team.py
    clinical_case = """I have a 78-year-old male patient with heart failure, diabetes, and kidney disease who presented with acute decompensation. His EF is 25% and he's currently on lisinopril, metoprolol, and furosemide.

BP 145/90, HR 110 irregular, JVD elevated, bilateral rales, S3 gallop, 2+ pitting edema bilaterally. Labs: BNP 850 pg/mL, creatinine 1.8 mg/dL, eGFR 35 mL/min/1.73m², sodium 138 mEq/L, potassium 4.2 mEq/L.

Left VEF 25%, severe global hypokinesis, MMR, estimated pasp 45 mmHg, LA 45 mL/m².

What's the best approach for optimizing his heart failure therapy?
    """
    
    # Sample evidence snippets
    evidence_snippets = [
        {
            "snippet_id": "hf_guidelines_1",
            "text": "Heart failure with reduced ejection fraction (HFrEF) management includes ACE inhibitors, beta-blockers, and diuretics.",
            "source_id": "acc_aha_2022",
            "source_type": "guideline",
            "source_url": "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001063"
        },
        {
            "snippet_id": "ckd_considerations_1", 
            "text": "In patients with chronic kidney disease, ACE inhibitors should be used cautiously due to risk of hyperkalemia and worsening renal function.",
            "source_id": "kdigo_2021",
            "source_type": "guideline",
            "source_url": "https://kdigo.org/guidelines/ckd-evaluation-and-management/"
        },
        {
            "snippet_id": "bnp_interpretation_1",
            "text": "BNP >400 pg/mL in patients with heart failure suggests significant volume overload and may indicate need for diuretic optimization.",
            "source_id": "heart_failure_guidelines_2023",
            "source_type": "guideline", 
            "source_url": "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001063"
        }
    ]
    
    try:
        sub_command = sys.argv[1] if len(sys.argv) > 1 else 'run'
        assert sub_command in ('run', 'persistence', 'mermaid')
    except (IndexError, AssertionError):
        print(
            'Usage:\n'
            '  uv run -m api.agents.pydantic_ai_team mermaid\n'
            'or:\n'
            '  uv run -m api.agents.pydantic_ai_team run\n'
            'or:\n'
            '  uv run -m api.agents.pydantic_ai_team persistence',
            file=sys.stderr,
        )
        sys.exit(1)

    if sub_command == 'mermaid':
        print(clinical_graph.mermaid_code(start_node=MultiSpecialistNode))
    elif sub_command == 'run':
        asyncio.run(run_clinical_diagnosis(clinical_case, evidence_snippets))
    else:  # persistence
        asyncio.run(run_with_persistence(clinical_case, evidence_snippets))