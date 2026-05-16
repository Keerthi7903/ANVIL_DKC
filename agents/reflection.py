import json
import time

from config import settings

from schemas.schemas import AgentResult

from utils.llm_clients import gemini_client

from utils.tracing import (
    trace_agent_start,
    trace_agent_end
)


async def run_reflection_agent(
    workflow_id: str,
    pr_number: int,
    repo: str,
    agent_results: list
) -> AgentResult:
    """
    Reflection agent that self-checks all findings before action.
    """

    start_time = time.time()

    trace_agent_start(
        "reflection",
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
                "contradictions": "none",
                "missing_info": "none",
                "confidence": "MEDIUM",
                "confidence_reasoning": (
                    "Most agents agree and sufficient data exists."
                )
            }

        else:

            prompt = f"""
You are reviewing findings from multiple AI agents.

PR #{pr_number} in repository {repo}

Agent Results:
{formatted_results}

Answer these questions:

1. Are there contradictions between agents?
2. Is important information missing?
3. Overall confidence:
HIGH / MEDIUM / LOW

Return ONLY valid JSON:

{{
    "contradictions": "description or none",
    "missing_info": "description or none",
    "confidence": "HIGH|MEDIUM|LOW",
    "confidence_reasoning": "one sentence"
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

        confidence_map = {
            "HIGH": 0.95,
            "MEDIUM": 0.7,
            "LOW": 0.4
        }

        confidence_score = confidence_map.get(
            parsed["confidence"],
            0.5
        )

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="reflection",
            status="success",
            findings=parsed,
            confidence=confidence_score,
            recommended_action=(
                "proceed"
                if parsed["confidence"] != "LOW"
                else "needs_review"
            ),
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=None
        )

        trace_agent_end(
            "reflection",
            result
        )

        return result

    except Exception as e:

        print("REFLECTION AGENT ERROR:")
        print(str(e))

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        result = AgentResult(
            agent_name="reflection",
            status="failed",
            findings={},
            confidence=0.0,
            recommended_action=None,
            duration_ms=duration_ms,
            tokens_used=0,
            error_message=str(e)
        )

        trace_agent_end(
            "reflection",
            result
        )

        return result