import json
import time

from config import settings

from schemas.schemas import AgentResult

from utils.llm_clients import gemini_client

from utils.tracing import (
    trace_agent_start,
    trace_agent_end
)


async def run_planner_agent(
    workflow_id: str,
    past_incidents: list,
    agent_results: list
) -> AgentResult:
    """
    Main orchestration and autonomous decision agent.
    """

    start_time = time.time()

    trace_agent_start(
        "planner",
        workflow_id
    )

    try:

        formatted_results = []

        for result in agent_results:
            formatted_results.append({
                "agent": result.agent_name,
                "findings": result.findings,
                "confidence": result.confidence,
                "recommended_action": result.recommended_action
            })

        # MOCK MODE
        if settings.USE_MOCK_AI:

            parsed = {
                "decision": "snooze",
                "reasoning": (
                    "PR is low urgency and recently updated."
                )
            }

        else:

            prompt = f"""
You are an autonomous AI operations agent.

You must make ONE final autonomous decision
without asking humans for confirmation.

Past Incidents:
{past_incidents}

Agent Findings:
{formatted_results}

Choose EXACTLY ONE action:

- auto_assign
- post_comment
- escalate
- snooze

Decision Rules:
- auto_assign:
  reviewers absent OR silent
  AND CI passing

- post_comment:
  CI failing
  AND active reviewers exist

- escalate:
  urgency_score > 7
  OR repeated stale PR author
  OR PR stale > 120h

- snooze:
  low urgency
  recently updated

Return ONLY valid JSON:

{{
    "decision": "auto_assign|post_comment|escalate|snooze",
    "reasoning": "one sentence explanation"
}}
"""

            response = gemini_client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            text_output = response.text.strip()

            cleaned = text_output.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()

            parsed = json.loads(cleaned)

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="planner",
            status="success",
            findings={
                "decision": parsed["decision"],
                "reasoning": parsed["reasoning"]
            },
            confidence=0.95,
            recommended_action=parsed["decision"],
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=None
        )

        trace_agent_end(
            "planner",
            result
        )

        return result

    except Exception as e:

        print("PLANNER AGENT ERROR:")
        print(str(e))

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="planner",
            status="failed",
            findings={},
            confidence=0.0,
            recommended_action=None,
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=str(e)
        )

        trace_agent_end(
            "planner",
            result
        )

        return result
    
    