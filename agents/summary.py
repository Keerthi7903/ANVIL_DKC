import time

from config import settings

from schemas.schemas import AgentResult

from utils.llm_clients import gemini_client

from utils.tracing import (
    trace_agent_start,
    trace_agent_end
)


async def run_summary_agent(
    workflow_id: str,
    pr_metadata,
    agent_results: list,
    decision: str,
    action_taken: dict
) -> AgentResult:
    """
    Generate human-readable workflow summary.
    """

    start_time = time.time()

    trace_agent_start(
        "summary",
        workflow_id
    )

    try:

        formatted_results = []

        for result in agent_results:
            formatted_results.append({
                "agent": result.agent_name,
                "findings": result.findings,
                "status": result.status
            })

        # MOCK MODE
        if settings.USE_MOCK_AI:

            summary_markdown = f"""
## What Happened

PR #{pr_metadata.pr_number} in repository
`{pr_metadata.repo}` was analyzed for inactivity.

## Why This PR Was Stale

The PR had low reviewer engagement and remained inactive.

## Action Taken & Recommendations

Decision taken: `{decision}`

Recommended next step:
Monitor PR activity and assign reviewers if needed.
"""

        else:

            prompt = f"""
Generate a concise incident report for this stale PR event.

PR:
{pr_metadata.pr_title}

Repository:
{pr_metadata.repo}

Author:
{pr_metadata.author}

Staleness:
{pr_metadata.staleness_hours} hours

Agent Findings:
{formatted_results}

Decision Taken:
{decision}

Action Executed:
{action_taken}

Write a markdown report with EXACTLY these sections:

## What Happened

## Why This PR Was Stale

## Action Taken & Recommendations

Keep it concise and professional.
"""

            response = gemini_client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            summary_markdown = response.text.strip()

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="summary",
            status="success",
            findings={
                "report_markdown": summary_markdown
            },
            confidence=0.95,
            recommended_action=None,
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=None
        )

        trace_agent_end(
            "summary",
            result
        )

        return result

    except Exception as e:

        print("SUMMARY AGENT ERROR:")
        print(str(e))

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="summary",
            status="failed",
            findings={},
            confidence=0.0,
            recommended_action=None,
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=str(e)
        )

        trace_agent_end(
            "summary",
            result
        )

        return result