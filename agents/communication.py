import json
import time

from config import settings

from schemas.schemas import AgentResult

from utils.llm_clients import gemini_client

from utils.tracing import (
    trace_agent_start,
    trace_agent_end
)


async def run_communication_analysis(
    workflow_id: str,
    comments: str
) -> AgentResult:
    """
    Analyze PR communication sentiment and engagement.
    """

    start_time = time.time()

    trace_agent_start(
        "communication",
        workflow_id
    )

    try:

        # MOCK MODE
        if settings.USE_MOCK_AI:

            parsed = {
                "sentiment": "neutral",
                "reviewer_engagement": "absent",
                "blocking_concerns": False,
                "summary": "No meaningful reviewer discussion yet."
            }

        else:

            prompt = f"""
You are analysing a GitHub Pull Request discussion.

Given this comment history:

{comments}

Return ONLY valid JSON in this exact format:

{{
    "sentiment": "positive|neutral|negative|absent",
    "reviewer_engagement": "active|silent|absent",
    "blocking_concerns": true,
    "summary": "one sentence summary"
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

        comment_count = len(comments.split("\n"))

        confidence = (
            0.9
            if comment_count >= 5
            else 0.5
        )

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="communication",
            status="success",
            findings=parsed,
            confidence=confidence,
            recommended_action=None,
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=None
        )

        trace_agent_end(
            "communication",
            result
        )

        return result

    except Exception as e:

        print("COMMUNICATION AGENT ERROR:")
        print(str(e))

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="communication",
            status="failed",
            findings={},
            confidence=0.0,
            recommended_action=None,
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=str(e)
        )

        trace_agent_end(
            "communication",
            result
        )

        return result