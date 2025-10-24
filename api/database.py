"""
Database models and connection for task step tracking.
"""
from datetime import datetime
from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String, DateTime, Text, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Create database engine
DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

class User(Base):
    """Model for tracking a user."""
    __tablename__ = "users"

    user_id = Column(String, index=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class ClinicalCase(Base):
    """Model for tracking a clinical case."""
    __tablename__ = "clinical_cases"

    case_id = Column(String, index=True, nullable=False)
    status = Column(String, nullable=False)  # pending, running, completed, failed
    title = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Message(Base):
    """Model for tracking a message."""
    __tablename__ = "messages"

    message_id = Column(String, index=True, nullable=False)
    user_id = Column(String, nullable=False)
    
    from_id = Column(String, nullable=False)
    message_type = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    payload_json = Column(JSON, nullable=True)
    stage = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def create_task_steps(job_id: str, step_names: list[str]):
    """Create initial task step records for a job."""
    with get_db() as db:
        for idx, step_name in enumerate(step_names, 1):
            step = TaskStep(
                job_id=job_id,
                step_number=idx,
                step_name=step_name,
                status="pending"
            )
            db.add(step)


def update_step_status(job_id: str, step_number: int, status: str,
                       output: str = None, error: str = None):
    """Update the status of a task step."""
    with get_db() as db:
        step = db.query(TaskStep).filter(
            TaskStep.job_id == job_id,
            TaskStep.step_number == step_number
        ).first()

        if step:
            step.status = status
            step.updated_at = datetime.utcnow()

            if status == "running" and not step.started_at:
                step.started_at = datetime.utcnow()

            if status in ["completed", "failed"]:
                step.completed_at = datetime.utcnow()
                if step.started_at:
                    step.duration = (step.completed_at - step.started_at).total_seconds()

            if output:
                step.output = output

            if error:
                step.error = error


def get_task_steps(job_id: str) -> list[dict]:
    """Get all steps for a specific job."""
    with get_db() as db:
        steps = db.query(TaskStep).filter(
            TaskStep.job_id == job_id
        ).order_by(TaskStep.step_number).all()

        return [step.to_dict() for step in steps]


def get_task_progress(job_id: str) -> dict:
    """Get progress summary for a task."""
    with get_db() as db:
        steps = db.query(TaskStep).filter(TaskStep.job_id == job_id).all()

        if not steps:
            return None

        total_steps = len(steps)
        completed_steps = sum(1 for s in steps if s.status == "completed")
        failed_steps = sum(1 for s in steps if s.status == "failed")
        running_steps = sum(1 for s in steps if s.status == "running")

        return {
            "job_id": job_id,
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "failed_steps": failed_steps,
            "running_steps": running_steps,
            "progress_percentage": (completed_steps / total_steps * 100) if total_steps > 0 else 0,
            "status": "completed" if completed_steps == total_steps else
                     "failed" if failed_steps > 0 else
                     "running" if running_steps > 0 else "pending"
        }
