import structlog
from datetime import datetime


log = structlog.get_logger()


def trace_event(name: str, data: dict):
    """
    Generic trace hook for future observability.
    """

    log.info(
        name,
        data=data,
        timestamp=datetime.utcnow().isoformat()
    )


def trace_agent_start(agent: str, workflow_id: str):
    """
    Logs when an agent starts execution.
    """

    log.info(
        "agent_start",
        agent=agent,
        workflow_id=workflow_id,
        timestamp=datetime.utcnow().isoformat()
    )


def trace_agent_end(agent: str, result):
    """
    Logs when an agent completes execution.
    """

    log.info(
        "agent_end",
        agent=agent,
        status=result.status,
        duration_ms=result.duration_ms,
        tokens_used=result.tokens_used,
        confidence=result.confidence,
        timestamp=datetime.utcnow().isoformat()
    )