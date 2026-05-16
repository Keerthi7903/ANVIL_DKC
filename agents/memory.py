import json

from typing import List, Dict

from schemas.schemas import WorkflowState

from utils.tracing import trace_event

from backend.database.database import (
    SessionLocal
)

from backend.database.models import (
    WorkflowRun
)


def retrieve(
    pr_author: str,
    repo: str,
    limit: int = 3
) -> List[Dict]:
    """
    Retrieve past incidents related
    to author or repo.
    """

    db = SessionLocal()

    try:

        workflows = (
            db.query(WorkflowRun)
            .filter(
                (WorkflowRun.author == pr_author)
                |
                (WorkflowRun.repo == repo)
            )
            .order_by(
                WorkflowRun.id.desc()
            )
            .limit(limit)
            .all()
        )

        results = []

        for item in workflows:

            results.append({
                "workflow_id": item.workflow_id,
                "author": item.author,
                "repo": item.repo,
                "decision": item.decision,
                "summary": item.summary,
                "status": item.status
            })

        trace_event(
            "memory_retrieve",
            {
                "author": pr_author,
                "repo": repo,
                "results_found": len(results)
            }
        )

        return results

    finally:

        db.close()


def persist(
    workflow_state: WorkflowState
) -> None:
    """
    Persist completed workflow
    into SQLite database.
    """

    db = SessionLocal()

    try:

        workflow = WorkflowRun(

            workflow_id=workflow_state.workflow_id,

            pr_title=(
                workflow_state.pr_metadata.pr_title
                if workflow_state.pr_metadata
                else "unknown"
            ),

            repo=(
                workflow_state.pr_metadata.repo
                if workflow_state.pr_metadata
                else "unknown"
            ),

            author=(
                workflow_state.pr_metadata.author
                if workflow_state.pr_metadata
                else "unknown"
            ),

            status=workflow_state.status,

            decision=workflow_state.decision,

            summary=workflow_state.summary,

            confidence=(
                workflow_state.agent_results[-1].confidence
                if workflow_state.agent_results
                else 0.0
            ),

            created_at="2026-05-16",

            pr_url=(
                workflow_state.pr_url
            ),

            agent_results=json.dumps([
                result.model_dump(
                    mode="json"
                )
                for result in
                workflow_state.agent_results
            ]),

            action_taken=json.dumps(
                workflow_state.action_taken
            ),

            labels=json.dumps(
                workflow_state.pr_metadata.labels
                if workflow_state.pr_metadata
                else []
            ),

            reviewers=json.dumps(
                workflow_state.pr_metadata.reviewers
                if workflow_state.pr_metadata
                else []
            ),

            reflection=workflow_state.reflection
        )

        db.add(workflow)

        db.commit()

        trace_event(
            "memory_persist",
            {
                "workflow_id": workflow_state.workflow_id,
                "decision": workflow_state.decision
            }
        )

    finally:

        db.close()