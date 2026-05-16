import time
from datetime import datetime, timedelta

from schemas.schemas import AgentResult

from tools.github_tools import (
    request_reviewer,
    post_pr_comment
)

from tools.discord_tools import (
    send_discord_alert,
    send_manager_escalation
)

from utils.tracing import (
    trace_agent_start,
    trace_agent_end
)


async def run_notification_agent(
    workflow_id: str,
    decision: str,
    pr_metadata: dict,
    reflection_reasoning: str = ""
) -> AgentResult:
    """
    Execute autonomous actions and notifications.
    """

    start_time = time.time()

    trace_agent_start(
        "notification",
        workflow_id
    )

    try:

        action_taken = {}

        owner = pr_metadata.owner
        repo = pr_metadata.repo
        pr_number = pr_metadata.pr_number

        # AUTO ASSIGN
        if decision == "auto_assign":

            reviewer = "octocat"

            success = await request_reviewer(
                owner,
                repo,
                pr_number,
                reviewer
            )

            action_taken = {
                "type": "reviewer_assigned",
                "reviewer": reviewer,
                "success": success
            }

            await send_discord_alert(
                f"🤖 Auto-assigned reviewer @{reviewer} "
                f"to PR #{pr_number}"
            )

        # POST COMMENT
        elif decision == "post_comment":

            comment_body = (
                f"🤖 AI Team OS detected inactivity "
                f"on this PR.\n\n"
                f"{reflection_reasoning}"
            )

            comment_url = await post_pr_comment(
                owner,
                repo,
                pr_number,
                comment_body
            )

            action_taken = {
                "type": "comment_posted",
                "comment_url": comment_url
            }

            await send_discord_alert(
                f"💬 Posted automated PR comment "
                f"on PR #{pr_number}"
            )

        # ESCALATE
        elif decision == "escalate":

            await send_manager_escalation(
                title=f"🚨 Escalation for PR #{pr_number}",
                description=(
                    f"PR requires managerial attention.\n\n"
                    f"{reflection_reasoning}"
                )
            )

            action_taken = {
                "type": "escalated",
                "channel": "manager"
            }

        # SNOOZE
        elif decision == "snooze":

            retry_at = (
                datetime.utcnow() +
                timedelta(hours=24)
            ).isoformat()

            action_taken = {
                "type": "snoozed",
                "retry_at": retry_at
            }

            await send_discord_alert(
                f"😴 Snoozed PR #{pr_number} for 24h"
            )

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="notification",
            status="success",
            findings=action_taken,
            confidence=1.0,
            recommended_action=decision,
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=None
        )

        trace_agent_end(
            "notification",
            result
        )

        return result

    except Exception as e:
        print("NOTIFICATION AGENT ERROR:")
        print(str(e))
        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="notification",
            status="failed",
            findings={},
            confidence=0.0,
            recommended_action=None,
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=str(e)
        )

        trace_agent_end(
            "notification",
            result
        )

        return result