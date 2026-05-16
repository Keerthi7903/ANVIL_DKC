import asyncio
import uuid
from datetime import datetime, timezone

from schemas.schemas import (
    WorkflowState,
    PRMetadata
)

from workflows.langgraph_workflow import graph


async def main():

    workflow_id = str(uuid.uuid4())

    pr_metadata = PRMetadata(
        pr_number=2,
        pr_title="Fix authentication timeout bug",
        pr_url="https://github.com/Keerthi7903/anviltest/pull/2",
        repo="anviltest",
        owner="Keerthi7903",
        author="dyuthi",
        created_at=datetime.now(timezone.utc),
        last_activity_at=datetime.now(timezone.utc),
        staleness_hours=72.0,
        reviewers=[],
        ci_status="passing",
        ci_error_message=None,
        labels=["bugfix", "urgent"],
        comment_count=0,
        body="Authentication timeout issue fix."
    )

    initial_state = WorkflowState(
        workflow_id=workflow_id,
        pr_url=pr_metadata.pr_url,
        pr_metadata=pr_metadata,
        status="running"
    )

    result = await graph.ainvoke(initial_state)

    print("\n")
    print("=" * 60)
    print("WORKFLOW COMPLETE")
    print("=" * 60)

    print(f"Workflow ID: {result['workflow_id']}")
    print(f"Decision: {result['decision']}")
    print(f"Status: {result['status']}")

    print("\nSUMMARY:\n")
    print(result["summary"])

    print("\nAGENTS EXECUTED:\n")

    for agent in result["agent_results"]:
        print(
            f"- {agent.agent_name} | "
            f"{agent.status} | "
            f"confidence={agent.confidence}"
        )


if __name__ == "__main__":
    asyncio.run(main())