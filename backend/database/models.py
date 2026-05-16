from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text
)

from backend.database.database import Base


class WorkflowRun(Base):

    __tablename__ = "workflow_runs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    workflow_id = Column(
        String,
        unique=True,
        index=True
    )

    # PR DETAILS
    pr_title = Column(String)

    repo = Column(String)

    author = Column(String)

    pr_url = Column(Text)

    # WORKFLOW STATUS
    status = Column(String)

    # NEW:
    # REAL PR LIFECYCLE STATE
    pr_state = Column(String)

    # AI DECISION
    decision = Column(String)

    summary = Column(Text)

    confidence = Column(Float)

    created_at = Column(String)

    # AGENT DATA
    agent_results = Column(Text)

    action_taken = Column(Text)

    labels = Column(Text)

    reviewers = Column(Text)

    reflection = Column(Text)