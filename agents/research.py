import time

from config import settings

from schemas.schemas import AgentResult

from tools.search_tools import tavily_search

from utils.llm_clients import gemini_client

from utils.tracing import (
    trace_agent_start,
    trace_agent_end
)


async def run_research_agent(
    workflow_id: str,
    pr_metadata
) -> AgentResult:
    """
    Research external engineering context
    related to PR topics.
    """

    start_time = time.time()

    trace_agent_start(
        "research",
        workflow_id
    )

    try:

        queries = []

        title = (
            pr_metadata.pr_title.lower()
            if pr_metadata.pr_title
            else ""
        )

        body = (
            pr_metadata.body.lower()
            if pr_metadata.body
            else ""
        )

        combined_text = (
            f"{title} {body}"
        )

        # =====================
        # SECURITY
        # =====================

        if any(
            keyword in combined_text
            for keyword in [
                "auth",
                "token",
                "jwt",
                "security",
                "login"
            ]
        ):

            queries.append(
                "JWT authentication security best practices"
            )

        # =====================
        # CI/CD
        # =====================

        if any(
            keyword in combined_text
            for keyword in [
                "ci",
                "pipeline",
                "workflow",
                "github actions"
            ]
        ):

            queries.append(
                "GitHub Actions CI reliability best practices"
            )

        # =====================
        # DATABASE
        # =====================

        if any(
            keyword in combined_text
            for keyword in [
                "database",
                "sql",
                "migration",
                "session"
            ]
        ):

            queries.append(
                "Database migration consistency best practices"
            )

        # =====================
        # DOCUMENTATION
        # =====================

        if any(
            keyword in combined_text
            for keyword in [
                "readme",
                "docs",
                "documentation"
            ]
        ):

            queries.append(
                "Engineering documentation review best practices"
            )

        # =====================
        # STALE PR
        # =====================

        if (
            pr_metadata.staleness_hours
            and pr_metadata.staleness_hours
            > 72
        ):

            queries.append(
                "GitHub pull request stale review SLA best practices"
            )

        all_results = []

        # =====================
        # RUN TAVILY SEARCHES
        # =====================

        for query in queries:

            try:

                results = await tavily_search(
                    query=query,
                    max_results=2
                )

                all_results.extend(
                    results
                )

            except Exception as search_error:

                print(
                    "TAVILY SEARCH ERROR:"
                )

                print(
                    str(search_error)
                )

        # =====================
        # NO RESEARCH NEEDED
        # =====================

        if not all_results:

            synthesis = (
                "No major external engineering "
                "risks detected for this PR."
            )

            confidence = 0.75

        # =====================
        # MOCK AI MODE
        # =====================

        elif settings.USE_MOCK_AI:

            synthesis_parts = []

            if "auth" in combined_text:

                synthesis_parts.append(
                    "Authentication-related logic detected. "
                    "Security validation and token expiry "
                    "handling should be reviewed carefully."
                )

            if "pipeline" in combined_text:

                synthesis_parts.append(
                    "CI/CD workflow modifications detected. "
                    "Deployment reliability and test stability "
                    "should be verified."
                )

            if "database" in combined_text:

                synthesis_parts.append(
                    "Database-related modifications may require "
                    "migration consistency checks."
                )

            if "docs" in combined_text or "readme" in combined_text:

                synthesis_parts.append(
                    "Documentation-focused PR detected with "
                    "low operational risk."
                )

            if not synthesis_parts:

                synthesis_parts.append(
                    "External engineering research completed "
                    "successfully."
                )

            synthesis = " ".join(
                synthesis_parts
            )

            confidence = 0.90

        # =====================
        # REAL GEMINI MODE
        # =====================

        else:

            synthesis_prompt = f"""
Analyze this GitHub Pull Request.

PR Title:
{pr_metadata.pr_title}

PR Description:
{pr_metadata.body}

External Research:
{all_results}

Provide:
- engineering risks
- recommendations
- operational concerns
- severity assessment
"""

            response = (
                gemini_client
                .models
                .generate_content(
                    model=
                    "gemini-3.1-flash-lite",

                    contents=
                    synthesis_prompt
                )
            )

            synthesis = (
                response.text.strip()
            )

            confidence = 0.95

        duration_ms = int(
            (time.time() - start_time)
            * 1000
        )

        result = AgentResult(

            agent_name="research",

            status="success",

            findings={

                "search_queries":
                    queries,

                "search_results":
                    all_results,

                "synthesis":
                    synthesis
            },

            confidence=confidence,

            recommended_action=None,

            duration_ms=duration_ms,

            tokens_used=0,

            error_message=None
        )

        trace_agent_end(
            "research",
            result
        )

        return result

    except Exception as e:

        print(
            "RESEARCH AGENT ERROR:"
        )

        print(str(e))

        duration_ms = int(
            (time.time() - start_time)
            * 1000
        )

        result = AgentResult(

            agent_name="research",

            status="failed",

            findings={},

            confidence=0.0,

            recommended_action=None,

            duration_ms=duration_ms,

            tokens_used=0,

            error_message=str(e)
        )

        trace_agent_end(
            "research",
            result
        )

        return result