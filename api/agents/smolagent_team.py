from smolagents import InferenceClientModel, CodeAgent, ActionStep, TaskStep, OpenAIServerModel
import os
from datetime import datetime
from smolagents.monitoring import Timing
from smolagents import tool, ToolCallingAgent
import random
from dotenv import load_dotenv

load_dotenv()

model = OpenAIServerModel(
    model_id="gpt-5-nano",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_BASE_URL"),
)

# let's build the agent workflow
multi_specialist_agent = CodeAgent(
    name="multi_specialist_agent",
    description="""You are a panel of board-certified specialists (cardiology, nephrology, endocrinology, infectious disease, geriatrics).
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
    model=model,
    tools=[],
)

warning_agent = CodeAgent(
    name="warning_agent",
    description="""You detect *immediate dangers* and *can't-miss diagnoses* (red flags) from the same inputs.

OUTPUT
- "red_flags": up to 5 bullets, each a short sentence with evidence <cite>snippet_id</cite>.
- "urgent_actions": up to 3 bullets (diagnostic stabilization ideas, not definitive treatment).

CONSTRAINTS
- Keep it brief. No probabilities.
- Use only evidence_snippets for citations.
- stage: "intermediate".
""",
    model=model,
    tools=[],
)

review_agent = CodeAgent(
    name="review_agent",
    description="""You merge (A) the multi-specialist differential and (B) the warning agent red flags.

OUTPUT
- A single prioritized differential list (top 5-8).
- For each diagnosis: one-line rationale with citations <cite>snippet_id</cite>.
- Mark any diagnosis that directly addresses a red flag.

CONSTRAINTS
- Do not add new diagnoses without evidence.
- stage: "intermediate".
""",
    model=model,
    tools=[],
)

verification_agent = CodeAgent(
    name="verification_agent",
    description="""You verify each diagnosis against contemporary clinical guidelines and major trial evidence *present in evidence_snippets*.

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
    model=model,
    tools=[],
)

reasoning_agent = CodeAgent(
    name="reasoning_agent",
    description="""You write the *detailed diagnostic narrative* for each verified diagnosis.

FOR EACH DIAGNOSIS (short section):
- "why_this": 2-4 sentences connecting findings → pathophysiology, with citations <cite>snippet_id</cite>.
- "why_not_others": ≤2 short bullets contrasting key alternatives, with citations.
- "evidence_list": 3-6 bullet points: quote short fragments or paraphrase + <cite>id</cite>.

STYLE
- Clear, clinical, concise; no treatment.
- Only cite available evidence_snippets.
- stage: "intermediate".
""",
    model=model,
    tools=[],
)

action_agent = CodeAgent(
    name="action_agent",
    description="""You propose a concise *treatment & next-step plan* tailored to the verified diagnoses and patient comorbidities.

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
    model=model,
    tools=[],
)

manager_agent = CodeAgent(
    name="manager_agent",
    description="""You orchestrate the full pipeline and return a single JSON as the final result.

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
    model=model,
    tools=[],
    managed_agents=[
        multi_specialist_agent,
        warning_agent,
        review_agent,
        verification_agent,
        reasoning_agent,
        action_agent,
    ]
)

if __name__ == "__main__":
    clinical_case = """I have a 78-year-old male patient with heart failure, diabetes, and kidney disease who presented with acute decompensation. His EF is 25% and he's currently on lisinopril, metoprolol, and furosemide.

BP 145/90, HR 110 irregular, JVD elevated, bilateral rales, S3 gallop, 2+ pitting edema bilaterally. Labs: BNP 850 pg/mL, creatinine 1.8 mg/dL, eGFR 35 mL/min/1.73m², sodium 138 mEq/L, potassium 4.2 mEq/L.

Left VEF 25%, severe global hypokinesis, MMR, estimated pasp 45 mmHg, LA 45 mL/m².

What's the best approach for optimizing his heart failure therapy?
    """
    
    manager_agent.run(clinical_case)