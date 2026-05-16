from pydantic import BaseModel
from typing import Literal, Optional, List, Dict, Any
from datetime import datetime


class AgentResult(BaseModel):
    agent_name: str
    status: Literal["success", "failed", "skipped"]
    findings: Dict[str, Any]
    confidence: float
    recommended_action: Optional[str]
    duration_ms: int
    tokens_used: int
    error_message: Optional[str] = None


class PRMetadata(BaseModel):
    pr_number: int
    pr_title: str
    pr_url: str
    repo: str
    owner: str
    author: str
    created_at: datetime
    last_activity_at: datetime
    staleness_hours: float
    reviewers: List[str]
    ci_status: Literal["passing", "failing", "pending", "none"]
    ci_error_message: Optional[str]
    labels: List[str]
    comment_count: int
    body: Optional[str]


class WorkflowState(BaseModel):
    workflow_id: str
    pr_url: str
    pr_metadata: Optional[PRMetadata] = None
    past_incidents: List[Dict] = []
    agent_results: List[AgentResult] = []
    reflection: str = ""
    confidence: Literal["high", "medium", "low"] = "medium"
    decision: Optional[
        Literal[
            "escalate",
            "auto_assign",
            "post_comment",
            "snooze"
        ]
    ] = None
    action_taken: Dict[str, Any] = {}
    summary: str = ""
    status: Literal[
        "pending",
        "running",
        "completed",
        "failed"
    ] = "pending"