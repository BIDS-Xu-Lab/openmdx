"""
API server for clinical case management with streaming support.
"""
import json
import time
import uuid
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from redis import Redis
from rq import Queue
from database import (
    init_db, create_case, get_case, get_case_full,
    get_new_messages, update_case_status
)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Redis connection for job queue
redis_conn = Redis(host='localhost', port=6379, db=0)
job_queue = Queue('clinical_cases', connection=redis_conn)


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


@app.route('/api/create_case', methods=['POST'])
def create_case_endpoint():
    """
    Create a new clinical case and enqueue processing job.

    Request body:
    {
        "question": "Patient question or case description",
        "title": "Optional case title"
    }

    Response:
    {
        "case_id": "uuid",
        "status": "CREATED",
        "title": "...",
        "created_at": "ISO timestamp"
    }
    """
    data = request.json
    question = data.get('question')
    title = data.get('title', question[:100] if question else "Untitled Case")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    # Generate unique case ID
    case_id = str(uuid.uuid4())

    # Create case in database
    case = create_case(case_id, title)

    # Enqueue job for processing
    job = job_queue.enqueue(
        'worker.process_case',
        case_id=case_id,
        question=question,
        job_timeout='10m'
    )

    return jsonify({
        "case_id": case.case_id,
        "status": case.status,
        "title": case.data_json.get("title"),
        "created_at": case.created_at.isoformat(),
        "job_id": job.id
    }), 201


@app.route('/api/cases/<case_id>', methods=['GET'])
def get_case_endpoint(case_id):
    """
    Get full case data including all messages and evidence snippets.

    Response:
    {
        "case_id": "uuid",
        "status": "CREATED|PROCESSING|COMPLETED|ERROR",
        "title": "...",
        "messages": [...],
        "evidence_snippets": [...],
        "created_at": "ISO timestamp",
        "updated_at": "ISO timestamp"
    }
    """
    case_data = get_case_full(case_id)

    if not case_data:
        return jsonify({"error": "Case not found"}), 404

    return jsonify(case_data)


@app.route('/api/cases/<case_id>/stream', methods=['GET'])
def stream_case_endpoint(case_id):
    """
    Server-Sent Events endpoint for streaming case updates.

    This endpoint keeps the connection open and sends new messages
    as they are added to the database by the worker.

    SSE format:
    data: {"type": "message", "data": {...}}

    data: {"type": "status", "status": "COMPLETED"}
    """
    def generate():
        # Verify case exists
        case = get_case(case_id)
        if not case:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Case not found'})}\n\n"
            return

        # Send initial status
        yield f"data: {json.dumps({'type': 'status', 'status': case.status})}\n\n"

        last_message_id = None
        max_iterations = 300  # 5 minutes max (300 * 1 second)
        iteration = 0

        while iteration < max_iterations:
            # Get case status
            case = get_case(case_id)
            if not case:
                break

            # Get new messages since last check
            new_messages = get_new_messages(case_id, last_message_id)

            # Send new messages
            for msg in new_messages:
                yield f"data: {json.dumps({'type': 'message', 'data': msg})}\n\n"
                last_message_id = msg['message_id']

            # Send status update
            yield f"data: {json.dumps({'type': 'status', 'status': case.status})}\n\n"

            # If case is completed or errored, send final event and close
            if case.status in ['COMPLETED', 'ERROR']:
                yield f"data: {json.dumps({'type': 'done', 'status': case.status})}\n\n"
                break

            # Wait before next check
            time.sleep(1)
            iteration += 1

        # Timeout or completion
        if iteration >= max_iterations:
            yield f"data: {json.dumps({'type': 'timeout'})}\n\n"

    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


@app.route('/api/cases', methods=['GET'])
def list_cases_endpoint():
    """
    List all cases (for development/testing).

    Response:
    {
        "cases": [...]
    }
    """
    from database import get_db, ClinicalCase

    with get_db() as db:
        cases = db.query(ClinicalCase).order_by(ClinicalCase.created_at.desc()).limit(50).all()
        return jsonify({
            "cases": [case.to_dict() for case in cases]
        })


def main():
    """Initialize database and run server."""
    init_db()
    print("Database initialized")
    print("Starting server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)


if __name__ == '__main__':
    main()
