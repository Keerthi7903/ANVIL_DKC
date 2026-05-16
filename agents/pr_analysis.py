from datetime import datetime, timezone
import time

from schemas.schemas import (
    AgentResult,
    PRMetadata
)

from tools.github_tools import (
    get_pr_details,
    list_pr_reviewers
)

from utils.tracing import (
    trace_agent_start,
    trace_agent_end
)


async def run_pr_analysis(
    workflow_id: str,
    owner: str,
    repo: str,
    pr_number: int
) -> AgentResult:
    """
    Analyze GitHub PR metadata and calculate staleness.
    """

    start_time = time.time()

    trace_agent_start(
        "pr_analysis",
        workflow_id
    )

    try:
        pr_data = await get_pr_details(
            owner,
            repo,
            pr_number
        )

        reviewers = await list_pr_reviewers(
            owner,
            repo,
            pr_number
        )

        created_at = datetime.fromisoformat(
            pr_data["created_at"].replace("Z", "+00:00")
        )

        updated_at = datetime.fromisoformat(
            pr_data["updated_at"].replace("Z", "+00:00")
        )

        now = datetime.now(timezone.utc)

        staleness_hours = (
            now - updated_at
        ).total_seconds() / 3600

        metadata = PRMetadata(
            pr_number=pr_data["number"],
            pr_title=pr_data["title"],
            pr_url=pr_data["html_url"],
            repo=repo,
            owner=owner,
            author=pr_data["user"]["login"],
            created_at=created_at,
            last_activity_at=updated_at,
            staleness_hours=staleness_hours,
            reviewers=reviewers,
            ci_status="pending",
            ci_error_message=None,
            labels=[
                label["name"]
                for label in pr_data.get("labels", [])
            ],
            comment_count=pr_data["comments"],
            body=pr_data.get("body")
        )

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="pr_analysis",
            status="success",
            findings=metadata.model_dump(),
            confidence=1.0,
            recommended_action=(
                "review_needed"
                if staleness_hours >= 24
                else None
            ),
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=None
        )

        trace_agent_end(
            "pr_analysis",
            result
        )

        return result

    except Exception as e:
        
        duration_ms = int(
            (time.time() - start_time) * 1000
        )
        print("PR ANALYSIS ERROR:")
        print(str(e))
        result = AgentResult(
            agent_name="pr_analysis",
            status="failed",
            findings={},
            confidence=0.0,
            recommended_action=None,
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=str(e)
        )

        trace_agent_end(
            "pr_analysis",
            result
        )

        return result