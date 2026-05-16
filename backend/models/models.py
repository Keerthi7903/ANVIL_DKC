from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime
)

from backend.database.database import Base


class WorkflowRun(Base):

    __tablename__ = "workflow_runs"

    id = Column(Integer, primary_key=True, index=True)

    workflow_id = Column(String, unique=True)

    pr_number = Column(Integer)

    repo = Column(String)

    owner = Column(String)

    author = Column(String)

    decision = Column(String)

    status = Column(String)

    summary = Column(Text)

    created_at = Column(DateTime)


class AgentRun(Base):

    __tablename__ = "agent_runs"

    id = Column(Integer, primary_key=True, index=True)

    workflow_id = Column(String)

    agent_name = Column(String)

    status = Column(String)

    confidence = Column(Float)

    recommended_action = Column(String)

    findings = Column(Text)

    error_message = Column(Text)