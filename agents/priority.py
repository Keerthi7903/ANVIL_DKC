import json
import time

from config import settings

from schemas.schemas import AgentResult

from utils.llm_clients import gemini_client

from utils.tracing import (
    trace_agent_start,
    trace_agent_end
)


async def run_priority_analysis(
    workflow_id: str,
    pr_data,
    communication_data: dict,
    past_incident_count: int
) -> AgentResult:
    """
    Analyze urgency and priority of stale PR.
    """

    start_time = time.time()

    trace_agent_start(
        "priority",
        workflow_id
    )

    try:

        # MOCK MODE
        if settings.USE_MOCK_AI:

            parsed = {
                "score": 3.5,
                "label": "low",
                "reason": (
                    "PR is recently updated and low urgency."
                )
            }

        else:

            prompt = f"""
You are a senior engineering manager scoring the urgency
of a stale GitHub Pull Request.

PR Data:
- Staleness Hours: {pr_data.staleness_hours}
- Reviewer Count: {len(pr_data.reviewers)}
- Reviewer Engagement: {communication_data.get("reviewer_engagement")}
- CI Status: {pr_data.ci_status}
- Labels: {pr_data.labels}
- Past Incidents By Author: {past_incident_count}

Return ONLY valid JSON:

{{
    "score": float,
    "label": "critical|high|medium|low",
    "reason": "one sentence"
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

        score = float(parsed["score"])

        confidence = (
            0.9
            if score > 7 or score < 3
            else 0.6
        )

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="priority",
            status="success",
            findings={
                "urgency_score": score,
                "urgency_label": parsed["label"],
                "reason": parsed["reason"]
            },
            confidence=confidence,
            recommended_action=(
                "escalate"
                if score >= 8
                else None
            ),
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=None
        )

        trace_agent_end(
            "priority",
            result
        )

        return result

    except Exception as e:

        print("PRIORITY AGENT ERROR:")
        print(str(e))

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="priority",
            status="failed",
            findings={},
            confidence=0.0,
            recommended_action=None,
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=str(e)
        )

        trace_agent_end(
            "priority",
            result
        )

        return result