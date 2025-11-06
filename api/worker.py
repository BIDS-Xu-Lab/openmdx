"""
RQ worker for processing clinical cases.

This module contains the job processing function and worker startup logic.
The worker listens to the Redis queue and processes jobs automatically.

To start the worker, run:
    python worker.py

The worker will:
1. Connect to Redis
2. Listen to the 'clinical_cases' queue
3. Process jobs as they arrive
4. Write results to the database in real-time
"""
import sys
import traceback
from datetime import datetime
from redis import Redis
from rq import Worker, Queue
from sqlmodel import Session
from database import (
    update_case_status, add_message, add_evidence_snippet,
    get_case, engine, init_db
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
        with Session(engine) as db:
            # Update status to PROCESSING
            update_case_status(db, case_id, "PROCESSING")
            print(f"[Worker] Case {case_id} status updated to PROCESSING")

            # Add user's question as first message
            user_msg_id = f"user_{case_id[:8]}"
            add_message(db, case_id, user_msg_id, {
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
            with Session(engine) as db:
                if item['type'] == 'message':
                    # Add message to database
                    msg_data = item['data']
                    add_message(db, case_id, msg_data['message_id'], {
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
                    add_evidence_snippet(db, case_id, evid_data['snippet_id'], {
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
        with Session(engine) as db:
            update_case_status(db, case_id, "COMPLETED")
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
            with Session(engine) as db:
                update_case_status(db, case_id, "ERROR")
                # Add error message
                add_message(db, case_id, f"error_{case_id[:8]}", {
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


def start_worker():
    """
    Start the RQ worker that listens to the clinical_cases queue.

    This function:
    1. Initializes the database
    2. Connects to Redis
    3. Creates the queue
    4. Starts the worker in blocking mode
    """
    print("=" * 60)
    print("Clinical Case Worker")
    print("=" * 60)

    # Initialize database
    print("\n[Init] Initializing database...")
    init_db()
    print("[Init] Database initialized successfully")

    # Connect to Redis
    print("\n[Redis] Connecting to Redis (localhost:6379)...")
    try:
        redis_conn = Redis(host='localhost', port=6379, db=0)
        redis_conn.ping()
        print("[Redis] Connected successfully")
    except Exception as e:
        print(f"[Error] Failed to connect to Redis: {e}")
        print("[Error] Make sure Redis is running: brew services start redis")
        sys.exit(1)

    # Create queue
    queue = Queue('clinical_cases', connection=redis_conn)
    print(f"\n[Queue] Listening to queue: 'clinical_cases'")
    print(f"[Queue] Current jobs in queue: {len(queue)}")

    # Start worker
    print("\n[Worker] Starting RQ worker...")
    print("[Worker] Press Ctrl+C to stop\n")
    print("=" * 60)

    try:
        worker = Worker([queue], connection=redis_conn)
        worker.work()
    except KeyboardInterrupt:
        print("\n\n[Worker] Shutting down gracefully...")
        print("[Worker] Worker stopped")
    except Exception as e:
        print(f"\n\n[Error] Worker error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Check if user wants to test a specific case
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test mode: python worker.py test <case_id> <question>
        if len(sys.argv) < 4:
            print("Test mode usage: python worker.py test <case_id> <question>")
            sys.exit(1)

        print("Running in test mode...")
        test_case_id = sys.argv[2]
        test_question = sys.argv[3]
        print(f"Testing with case_id={test_case_id}, question={test_question}")
        result = process_case(test_case_id, test_question)
        print(f"Result: {result}")
    else:
        # Normal mode: Start the worker
        start_worker()
