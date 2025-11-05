"""
Database models and connection for clinical case tracking.
Uses SQLite with JSON blobs for flexibility.
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from contextlib import contextmanager

# Create database engine
DATABASE_URL = "sqlite:///./clinical_cases.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class ClinicalCase(Base):
    """Model for tracking a clinical case."""
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, nullable=False)  # CREATED, PROCESSING, COMPLETED, ERROR
    data_json = Column(JSON, nullable=False)  # Contains: title, etc.
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = relationship("Message", back_populates="case", cascade="all, delete-orphan")
    evidence_snippets = relationship("EvidenceSnippet", back_populates="case", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "case_id": self.case_id,
            "status": self.status,
            "title": self.data_json.get("title"),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Message(Base):
    """Model for tracking a message in a case."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String, unique=True, index=True, nullable=False)
    case_id = Column(String, ForeignKey("cases.case_id"), nullable=False, index=True)
    message_data_json = Column(JSON, nullable=False)  # Contains: from_id, message_type, text, payload_json, stage
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    case = relationship("ClinicalCase", back_populates="messages")

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "case_id": self.case_id,
            "from_id": self.message_data_json.get("from_id"),
            "message_type": self.message_data_json.get("message_type"),
            "text": self.message_data_json.get("text"),
            "payload_json": self.message_data_json.get("payload_json"),
            "stage": self.message_data_json.get("stage"),
            "created_at": self.created_at.isoformat(),
        }


class EvidenceSnippet(Base):
    """Model for tracking evidence snippets in a case."""
    __tablename__ = "evidence_snippets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    snippet_id = Column(String, unique=True, index=True, nullable=False)
    case_id = Column(String, ForeignKey("cases.case_id"), nullable=False, index=True)
    snippet_data_json = Column(JSON, nullable=False)  # Contains: text, source_id, source_type, source_url, source_citation, index
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    case = relationship("ClinicalCase", back_populates="evidence_snippets")

    def to_dict(self):
        return {
            "snippet_id": self.snippet_id,
            "case_id": self.case_id,
            "index": self.snippet_data_json.get("index", 0),
            "text": self.snippet_data_json.get("text"),
            "source_id": self.snippet_data_json.get("source_id"),
            "source_type": self.snippet_data_json.get("source_type"),
            "source_url": self.snippet_data_json.get("source_url"),
            "source_citation": self.snippet_data_json.get("source_citation"),
            "created_at": self.created_at.isoformat(),
        }


@contextmanager
def get_db():
    """Get database session context manager."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def create_case(case_id: str, title: str = None) -> ClinicalCase:
    """Create a new clinical case."""
    with get_db() as db:
        case = ClinicalCase(
            case_id=case_id,
            status="CREATED",
            data_json={"title": title}
        )
        db.add(case)
        db.flush()
        db.refresh(case)
        return case


def get_case(case_id: str) -> ClinicalCase:
    """Get a clinical case by ID."""
    with get_db() as db:
        case = db.query(ClinicalCase).filter(ClinicalCase.case_id == case_id).first()
        return case


def update_case_status(case_id: str, status: str):
    """Update the status of a case."""
    with get_db() as db:
        case = db.query(ClinicalCase).filter(ClinicalCase.case_id == case_id).first()
        if case:
            case.status = status
            case.updated_at = datetime.utcnow()


def add_message(case_id: str, message_id: str, message_data: dict):
    """Add a message to a case."""
    with get_db() as db:
        message = Message(
            message_id=message_id,
            case_id=case_id,
            message_data_json=message_data
        )
        db.add(message)


def add_evidence_snippet(case_id: str, snippet_id: str, snippet_data: dict):
    """Add an evidence snippet to a case."""
    with get_db() as db:
        snippet = EvidenceSnippet(
            snippet_id=snippet_id,
            case_id=case_id,
            snippet_data_json=snippet_data
        )
        db.add(snippet)


def get_case_full(case_id: str) -> dict:
    """Get full case data including messages and evidence snippets."""
    with get_db() as db:
        case = db.query(ClinicalCase).filter(ClinicalCase.case_id == case_id).first()
        if not case:
            return None

        messages = db.query(Message).filter(Message.case_id == case_id).order_by(Message.created_at).all()
        snippets = db.query(EvidenceSnippet).filter(EvidenceSnippet.case_id == case_id).order_by(EvidenceSnippet.created_at).all()

        return {
            "case_id": case.case_id,
            "status": case.status,
            "title": case.data_json.get("title"),
            "messages": [msg.to_dict() for msg in messages],
            "evidence_snippets": [snip.to_dict() for snip in snippets],
            "created_at": case.created_at.isoformat(),
            "updated_at": case.updated_at.isoformat(),
        }


def get_new_messages(case_id: str, since_message_id: str = None) -> list:
    """Get new messages for a case since a given message ID."""
    with get_db() as db:
        query = db.query(Message).filter(Message.case_id == case_id)

        if since_message_id:
            # Get messages created after the specified message
            since_msg = db.query(Message).filter(Message.message_id == since_message_id).first()
            if since_msg:
                query = query.filter(Message.created_at > since_msg.created_at)

        messages = query.order_by(Message.created_at).all()
        return [msg.to_dict() for msg in messages]
