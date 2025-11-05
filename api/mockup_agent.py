"""
Mockup agent that simulates clinical case analysis with evidence generation.
"""
import time
import uuid
from typing import Generator, Dict, List
from datetime import datetime


def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())[:12]


class MockupAgent:
    """
    Mockup agent that simulates multi-step reasoning with evidence snippets.
    """

    def __init__(self):
        self.evidence_snippets = []

    def process_question(self, question: str) -> Generator[Dict, None, None]:
        """
        Process a clinical question and yield messages and evidence snippets.

        Yields:
            Dict with 'type' ('message' or 'evidence') and 'data'
        """
        # Step 1: System thinking message
        time.sleep(0.5)
        yield {
            'type': 'message',
            'data': {
                'message_id': generate_id(),
                'from_id': 'system',
                'message_type': 'SYSTEM',
                'text': '',
                'payload_json': {
                    'event_name': 'agent_thinking',
                    'agent_id': 'clinical_agent',
                    'status': 'analyzing_case'
                },
                'stage': 'thinking',
                'created_at': datetime.utcnow().isoformat()
            }
        }

        # Step 2: Agent planning message
        time.sleep(0.5)
        evid_001 = generate_id()
        self._add_evidence_snippet(evid_001, {
            'snippet_id': evid_001,
            'index': 0,
            'text': f'Clinical question received: {question[:200]}...',
            'source_id': 'user_input_001',
            'source_type': 'clinical_note',
            'source_citation': 'User-provided clinical question',
            'created_at': datetime.utcnow().isoformat()
        })

        yield {
            'type': 'evidence',
            'data': self.evidence_snippets[-1]
        }

        yield {
            'type': 'message',
            'data': {
                'message_id': generate_id(),
                'from_id': 'clinical_agent',
                'message_type': 'AGENT',
                'text': f'I\'ll analyze this clinical question systematically. Let me search for relevant guidelines and evidence. <cite>{evid_001}</cite>',
                'payload_json': {
                    'agent_name': 'Clinical Agent'
                },
                'stage': 'planning',
                'created_at': datetime.utcnow().isoformat()
            }
        }

        # Step 3: Tool calling - guideline search
        time.sleep(0.8)
        yield {
            'type': 'message',
            'data': {
                'message_id': generate_id(),
                'from_id': 'system',
                'message_type': 'SYSTEM',
                'text': '',
                'payload_json': {
                    'event_name': 'tool_calling',
                    'tool_name': 'guideline_search',
                    'parameters': {
                        'query': question[:50]
                    }
                },
                'stage': 'tooling',
                'created_at': datetime.utcnow().isoformat()
            }
        }

        # Step 4: Tool result with evidence
        time.sleep(1.0)
        evid_002 = generate_id()
        self._add_evidence_snippet(evid_002, {
            'snippet_id': evid_002,
            'index': 1,
            'text': 'Current clinical guidelines recommend evidence-based approaches considering patient-specific factors including comorbidities, contraindications, and individual risk profiles. Treatment should be tailored to achieve optimal outcomes while minimizing adverse effects.',
            'source_id': 'guideline_2024_001',
            'source_type': 'clinical_guideline',
            'source_url': 'https://example.org/guidelines/2024',
            'source_citation': 'Medical Society. Clinical Practice Guidelines 2024.',
            'created_at': datetime.utcnow().isoformat()
        })

        yield {
            'type': 'evidence',
            'data': self.evidence_snippets[-1]
        }

        yield {
            'type': 'message',
            'data': {
                'message_id': generate_id(),
                'from_id': 'guideline_tool',
                'message_type': 'TOOL',
                'text': 'Retrieved current clinical guidelines with evidence-based recommendations for this condition.',
                'payload_json': {
                    'tool_name': 'Guideline Search',
                    'tool_parameters': {'query': question[:50]},
                    'tool_response': {'guidelines_found': 3, 'key_recommendations': 8}
                },
                'stage': 'tooling',
                'created_at': datetime.utcnow().isoformat()
            }
        }

        # Step 5: Evidence search
        time.sleep(1.0)
        yield {
            'type': 'message',
            'data': {
                'message_id': generate_id(),
                'from_id': 'system',
                'message_type': 'SYSTEM',
                'text': '',
                'payload_json': {
                    'event_name': 'tool_calling',
                    'tool_name': 'evidence_search',
                    'parameters': {
                        'query': 'clinical trials'
                    }
                },
                'stage': 'tooling',
                'created_at': datetime.utcnow().isoformat()
            }
        }

        # Step 6: Evidence search results
        time.sleep(1.2)
        evid_003 = generate_id()
        self._add_evidence_snippet(evid_003, {
            'snippet_id': evid_003,
            'index': 2,
            'text': 'Recent randomized controlled trials have demonstrated significant clinical benefits with favorable safety profiles. Meta-analysis of multiple studies shows consistent efficacy across diverse patient populations (HR 0.75, 95% CI 0.68-0.84, p<0.001). Number needed to treat is approximately 18 patients over 2 years.',
            'source_id': '31234567',
            'source_type': 'pubmed',
            'source_url': 'https://pubmed.ncbi.nlm.nih.gov/31234567/',
            'source_citation': 'Author A, et al. Clinical Trial Results. N Engl J Med. 2023;388:1234-1245.',
            'created_at': datetime.utcnow().isoformat()
        })

        yield {
            'type': 'evidence',
            'data': self.evidence_snippets[-1]
        }

        yield {
            'type': 'message',
            'data': {
                'message_id': generate_id(),
                'from_id': 'evidence_tool',
                'message_type': 'TOOL',
                'text': 'Found high-quality evidence from randomized controlled trials supporting the intervention.',
                'payload_json': {
                    'tool_name': 'Evidence Search',
                    'tool_parameters': {'query': 'clinical trials'},
                    'tool_response': {
                        'trials_found': 5,
                        'quality': 'high',
                        'primary_outcome': 'significant'
                    }
                },
                'stage': 'tooling',
                'created_at': datetime.utcnow().isoformat()
            }
        }

        # Step 7: Agent analysis
        time.sleep(0.8)
        yield {
            'type': 'message',
            'data': {
                'message_id': generate_id(),
                'from_id': 'clinical_agent',
                'message_type': 'AGENT',
                'text': f'Based on the evidence, I can now formulate comprehensive recommendations. <cite>{evid_002}</cite> <cite>{evid_003}</cite>',
                'payload_json': {
                    'agent_name': 'Clinical Agent'
                },
                'stage': 'planning',
                'created_at': datetime.utcnow().isoformat()
            }
        }

        # Step 8: Safety check
        time.sleep(0.8)
        evid_004 = generate_id()
        self._add_evidence_snippet(evid_004, {
            'snippet_id': evid_004,
            'index': 3,
            'text': 'Safety monitoring is essential. Common adverse effects are generally mild and self-limiting. Serious adverse events are rare (incidence <1%). Regular monitoring of laboratory parameters and clinical assessment is recommended during treatment.',
            'source_id': 'safety_review_2024',
            'source_type': 'clinical_guideline',
            'source_citation': 'Safety Review Committee. Safety Profile Analysis 2024.',
            'created_at': datetime.utcnow().isoformat()
        })

        yield {
            'type': 'evidence',
            'data': self.evidence_snippets[-1]
        }

        yield {
            'type': 'message',
            'data': {
                'message_id': generate_id(),
                'from_id': 'safety_tool',
                'message_type': 'TOOL',
                'text': 'Safety profile reviewed. Overall favorable risk-benefit ratio with appropriate monitoring.',
                'payload_json': {
                    'tool_name': 'Safety Checker',
                    'tool_response': {
                        'risk_level': 'low',
                        'monitoring_required': True
                    }
                },
                'stage': 'tooling',
                'created_at': datetime.utcnow().isoformat()
            }
        }

        # Step 9: System notification
        time.sleep(0.5)
        yield {
            'type': 'message',
            'data': {
                'message_id': generate_id(),
                'from_id': 'system',
                'message_type': 'SYSTEM',
                'text': '',
                'payload_json': {
                    'event_name': 'system_notification',
                    'status': 'analysis_complete',
                    'summary': 'Multi-step analysis completed with evidence synthesis'
                },
                'stage': 'summarizing',
                'created_at': datetime.utcnow().isoformat()
            }
        }

        # Step 10: Final answer
        time.sleep(1.0)
        final_text = self._generate_final_answer(question, evid_001, evid_002, evid_003, evid_004)

        yield {
            'type': 'message',
            'data': {
                'message_id': generate_id(),
                'from_id': 'clinical_agent',
                'message_type': 'AGENT',
                'text': final_text,
                'payload_json': {
                    'agent_name': 'Clinical Agent'
                },
                'stage': 'final',
                'created_at': datetime.utcnow().isoformat()
            }
        }

    def _add_evidence_snippet(self, snippet_id: str, data: Dict):
        """Add an evidence snippet to internal storage."""
        self.evidence_snippets.append(data)

    def _generate_final_answer(self, question: str, *evidence_ids: str) -> str:
        """Generate a comprehensive final answer with citations."""
        citations = ' '.join([f'<cite>{eid}</cite>' for eid in evidence_ids])

        return f"""## Clinical Recommendation

Based on your question: "{question[:100]}{'...' if len(question) > 100 else ''}"

### Assessment
The clinical scenario requires careful consideration of evidence-based approaches. {citations}

### Recommendations

1. **Initial Approach**
   - Begin with guideline-directed therapy as supported by current evidence <cite>{evidence_ids[1]}</cite>
   - Consider patient-specific factors including comorbidities and contraindications <cite>{evidence_ids[0]}</cite>

2. **Evidence-Based Intervention**
   - Clinical trials demonstrate significant benefit with favorable outcomes <cite>{evidence_ids[2]}</cite>
   - The intervention shows consistent efficacy across diverse populations
   - Number needed to treat is approximately 18 patients over 2 years

3. **Safety Considerations**
   - Monitor for adverse effects, though serious events are rare (<1%) <cite>{evidence_ids[3]}</cite>
   - Regular follow-up and laboratory monitoring as clinically indicated
   - Patient education regarding warning signs and when to seek care

4. **Follow-Up Plan**
   - Schedule reassessment in appropriate timeframe based on clinical context
   - Adjust therapy as needed based on response and tolerability
   - Consider specialist consultation if response is suboptimal

### Summary
This approach integrates current guidelines, high-quality evidence, and safety considerations to provide comprehensive care. {citations}"""


def simulate_agent_work(question: str) -> List[Dict]:
    """
    Simulate agent processing and return all results.

    Returns:
        List of dicts with 'type' and 'data' keys
    """
    agent = MockupAgent()
    results = []

    for item in agent.process_question(question):
        results.append(item)

    return results, agent.evidence_snippets
