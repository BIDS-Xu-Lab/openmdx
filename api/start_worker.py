#!/usr/bin/env python
"""
Helper script to start RQ worker for processing clinical cases.

Usage:
    python start_worker.py
"""
from redis import Redis
from rq import Worker, Queue
from database import init_db

# Initialize database
print("Initializing database...")
init_db()

# Redis connection
redis_conn = Redis(host='localhost', port=6379, db=0)

# Create queue
queue = Queue('clinical_cases', connection=redis_conn)

print("Starting RQ worker for 'clinical_cases' queue...")
print("Listening for jobs...")
print("Press Ctrl+C to stop")

# Start worker
worker = Worker([queue], connection=redis_conn)
worker.work()
