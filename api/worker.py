"""
RQ worker for processing clinical cases.

This module contains the job processing function that will be executed by RQ workers.
The worker calls the mockup agent and writes results to the database.

To start a worker, run:
    rq worker clinical_cases --with-scheduler

Or use the start_worker.py script.
"""
import sys
import traceback
from datetime import datetime
from database import (
    update_case_status, add_message, add_evidence_snippet,
    get_case
)
from mockup_agent import MockupAgent


def process_case(case_id: str, question: str):
    """
    Process a clinical case using the mockup agent.

    This function is called by RQ worker to process cases asynchronously.

    Args:
        case_id: Unique identifier for the case
        question: Clinical question to analyze

    The function:
    1. Updates case status to PROCESSING
    2. Adds the user's question as the first message
    3. Processes the question with the mockup agent
    4. Writes messages and evidence snippets to the database as they're generated
    5. Updates case status to COMPLETED or ERROR
    """
    print(f"[Worker] Starting processing for case {case_id}")

    try:
        # Update status to PROCESSING
        update_case_status(case_id, "PROCESSING")
        print(f"[Worker] Case {case_id} status updated to PROCESSING")

        # Add user's question as first message
        user_msg_id = f"user_{case_id[:8]}"
        add_message(case_id, user_msg_id, {
            'from_id': 'user',
            'message_type': 'USER',
            'text': question,
            'payload_json': {},
            'stage': 'final',
            'created_at': datetime.utcnow().isoformat()
        })
        print(f"[Worker] Added user message for case {case_id}")

        # Process with mockup agent
        agent = MockupAgent()
        message_count = 0
        evidence_count = 0

        for item in agent.process_question(question):
            if item['type'] == 'message':
                # Add message to database
                msg_data = item['data']
                add_message(case_id, msg_data['message_id'], {
                    'from_id': msg_data['from_id'],
                    'message_type': msg_data['message_type'],
                    'text': msg_data.get('text', ''),
                    'payload_json': msg_data.get('payload_json', {}),
                    'stage': msg_data.get('stage', 'intermediate'),
                    'created_at': msg_data['created_at']
                })
                message_count += 1
                print(f"[Worker] Added message {message_count} ({msg_data['message_type']}/{msg_data.get('stage')}) for case {case_id}")

            elif item['type'] == 'evidence':
                # Add evidence snippet to database
                evid_data = item['data']
                add_evidence_snippet(case_id, evid_data['snippet_id'], {
                    'index': evid_data.get('index', 0),
                    'text': evid_data['text'],
                    'source_id': evid_data['source_id'],
                    'source_type': evid_data['source_type'],
                    'source_url': evid_data.get('source_url'),
                    'source_citation': evid_data.get('source_citation'),
                    'created_at': evid_data['created_at']
                })
                evidence_count += 1
                print(f"[Worker] Added evidence snippet {evidence_count} for case {case_id}")

        # Update status to COMPLETED
        update_case_status(case_id, "COMPLETED")
        print(f"[Worker] Case {case_id} completed successfully")
        print(f"[Worker] Summary: {message_count} messages, {evidence_count} evidence snippets")

        return {
            "success": True,
            "case_id": case_id,
            "messages": message_count,
            "evidence_snippets": evidence_count
        }

    except Exception as e:
        # Log error and update status
        error_msg = f"Error processing case {case_id}: {str(e)}"
        print(f"[Worker] ERROR: {error_msg}")
        traceback.print_exc()

        try:
            update_case_status(case_id, "ERROR")
            # Add error message
            add_message(case_id, f"error_{case_id[:8]}", {
                'from_id': 'system',
                'message_type': 'SYSTEM',
                'text': f'An error occurred during processing: {str(e)}',
                'payload_json': {
                    'event_name': 'error',
                    'error': str(e),
                    'traceback': traceback.format_exc()
                },
                'stage': 'final',
                'created_at': datetime.utcnow().isoformat()
            })
        except Exception as db_error:
            print(f"[Worker] ERROR: Failed to update database with error status: {str(db_error)}")

        return {
            "success": False,
            "case_id": case_id,
            "error": str(e)
        }


# For testing the worker directly
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python worker.py <case_id> <question>")
        sys.exit(1)

    test_case_id = sys.argv[1]
    test_question = sys.argv[2]

    print(f"Testing worker with case_id={test_case_id}, question={test_question}")
    result = process_case(test_case_id, test_question)
    print(f"Result: {result}")
