import json
import uuid

from fastapi import (
    FastAPI,
    Request
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from schemas.schemas import (
    WorkflowState,
    PRMetadata
)

from workflows.langgraph_workflow import graph

from backend.database.database import (
    SessionLocal
)

from backend.database.models import (
    WorkflowRun
)


app = FastAPI(
    title="AI Team OS Backend"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScenarioRequest(BaseModel):
    scenario: str


@app.get("/")
async def root():

    return {
        "message": "AI Team OS Backend Running"
    }


# =========================
# GET ALL WORKFLOWS
# =========================

@app.get("/workflows")
async def get_workflows():

    db: Session = SessionLocal()

    try:

        workflows = (
            db.query(WorkflowRun)
            .order_by(
                WorkflowRun.id.desc()
            )
            .all()
        )

        results = []

        for workflow in workflows:

            results.append({
                "workflow_id":
                    workflow.workflow_id,

                "title":
                    workflow.pr_title,

                "repo":
                    workflow.repo,

                "author":
                    workflow.author,

                "status":
                    workflow.status,
                
                "pr_state":
                    workflow.pr_state,

                "decision":
                    workflow.decision,

                "summary":
                    workflow.summary,

                "confidence":
                    workflow.confidence,

                "created_at":
                    workflow.created_at
            })

        return results

    finally:

        db.close()


# =========================
# GET SINGLE WORKFLOW
# =========================

@app.get(
    "/workflows/{workflow_id}"
)
async def get_workflow(
    workflow_id: str
):

    db: Session = SessionLocal()

    try:

        workflow = (
            db.query(WorkflowRun)
            .filter(
                WorkflowRun.workflow_id
                == workflow_id
            )
            .first()
        )

        if not workflow:

            return {
                "error":
                    "Workflow not found"
            }

        return {

            "workflow_id":
                workflow.workflow_id,

            "title":
                workflow.pr_title,

            "repo":
                workflow.repo,

            "author":
                workflow.author,

            "status":
                workflow.status,

            "pr_state":
                workflow.pr_state,

            "decision":
                workflow.decision,

            "summary":
                workflow.summary,

            "confidence":
                workflow.confidence,

            "created_at":
                workflow.created_at,

            "pr_url":
                workflow.pr_url,

            "reflection":
                workflow.reflection,

            "agent_results":
                json.loads(
                    workflow.agent_results
                )
                if workflow.agent_results
                else [],

            "action_taken":
                json.loads(
                    workflow.action_taken
                )
                if workflow.action_taken
                else {},

            "labels":
                json.loads(
                    workflow.labels
                )
                if workflow.labels
                else [],

            "reviewers":
                json.loads(
                    workflow.reviewers
                )
                if workflow.reviewers
                else []
        }

    finally:

        db.close()


@app.post("/simulate/stale-pr")
async def simulate_stale_pr(
    request: ScenarioRequest
):

    workflow_id = str(uuid.uuid4())

    pr_title = "Fix authentication timeout bug"

    staleness_hours = 72.0

    ci_status = "passing"

    reviewers = []

    labels = ["bugfix"]

    if request.scenario == "CI Failing":

        ci_status = "failing"

        labels = [
            "urgent",
            "ci-failure"
        ]

        pr_title = (
            "Critical CI Pipeline Failure"
        )

    elif request.scenario == (
        "Repeat Offender"
    ):

        staleness_hours = 168.0

        labels = [
            "stale",
            "high-priority"
        ]

        pr_title = (
            "Repeated Stale PR Incident"
        )

    elif request.scenario == (
        "No Reviewers"
    ):

        reviewers = []

        staleness_hours = 72.0

    pr_metadata = PRMetadata(
        pr_number=101,
        pr_title=pr_title,
        pr_url=(
            "https://github.com/"
            "demo/repo/pull/101"
        ),
        repo="demo-repo",
        owner="demo-owner",
        author="dyuthi",
        created_at=(
            "2026-05-15T10:00:00Z"
        ),
        last_activity_at=(
            "2026-05-15T10:00:00Z"
        ),
        staleness_hours=(
            staleness_hours
        ),
        reviewers=reviewers,
        ci_status=ci_status,
        ci_error_message=None,
        labels=labels,
        comment_count=0,
        body=(
            "Autonomous PR simulation."
        )
    )

    initial_state = WorkflowState(
        workflow_id=workflow_id,
        pr_url=pr_metadata.pr_url,
        pr_metadata=pr_metadata,
        status="running"
    )

    result = await graph.ainvoke(
        initial_state
    )

    return result


@app.post("/webhooks/github")
async def github_webhook(
    request: Request
):

    payload = await request.json()

    event = request.headers.get(
        "X-GitHub-Event",
        "unknown"
    )

    print("\n====================")
    print("GITHUB WEBHOOK RECEIVED")
    print("====================")

    print(f"EVENT: {event}")

    action = payload.get(
        "action"
    )

    print(f"ACTION: {action}")

    # =========================
    # PR OPENED
    # =========================

    if (
        event == "pull_request"
        and action == "opened"
    ):

        pr = payload["pull_request"]

        repo_data = payload[
            "repository"
        ]

        owner = repo_data[
            "owner"
        ]["login"]

        repo = repo_data["name"]

        workflow_id = str(
            uuid.uuid4()
        )

        created_at = pr[
            "created_at"
        ].replace(
            "Z",
            "+00:00"
        )

        updated_at = pr[
            "updated_at"
        ].replace(
            "Z",
            "+00:00"
        )

        pr_metadata = PRMetadata(
            pr_number=pr["number"],
            pr_title=pr["title"],
            pr_url=pr["html_url"],
            repo=repo,
            owner=owner,
            author=pr["user"]["login"],
            created_at=created_at,
            last_activity_at=updated_at,
            staleness_hours=0.0,
            reviewers=[],
            ci_status="pending",
            ci_error_message=None,
            labels=[
                label["name"]
                for label in pr.get(
                    "labels",
                    []
                )
            ],
            comment_count=pr[
                "comments"
            ],
            body=pr.get("body")
        )

        initial_state = WorkflowState(
            workflow_id=workflow_id,
            pr_url=pr_metadata.pr_url,
            pr_metadata=pr_metadata,
            status="running"
        )

        print(
            "\nSTARTING AI WORKFLOW..."
        )

        result = await graph.ainvoke(
            initial_state
        )

        print(
            "WORKFLOW COMPLETE"
        )

        return {
            "status":
                "workflow_triggered",

            "workflow_id":
                workflow_id,

            "decision":
                result.get(
                    "decision"
                )
        }


    # =========================
    # PR MERGED / CLOSED
    # =========================

    elif (
        event == "pull_request"
        and action == "closed"
    ):

        pr = payload["pull_request"]

        pr_url = pr["html_url"]

        merged = pr.get(
            "merged",
            False
        )

        db: Session = SessionLocal()

        try:

            workflow = (
                db.query(WorkflowRun)
                .filter(
                    WorkflowRun.pr_url
                    == pr_url
                )
                .order_by(
                    WorkflowRun.id.desc()
                )
                .first()
            )

            if workflow:

                workflow.pr_state = (
                    "merged"
                    if merged
                    else "closed"
                )

                db.commit()

                print(
                    f"PR STATE UPDATED: "
                    f"{workflow.pr_state}"
                )

            return {
                "status":
                    "pr_state_updated",

                "pr_state":
                    (
                        "merged"
                        if merged
                        else "closed"
                    )
            }

        finally:

            db.close()

        pr = payload["pull_request"]

        repo_data = payload[
            "repository"
        ]

        owner = repo_data[
            "owner"
        ]["login"]

        repo = repo_data["name"]

        workflow_id = str(
            uuid.uuid4()
        )

        created_at = pr[
            "created_at"
        ].replace(
            "Z",
            "+00:00"
        )

        updated_at = pr[
            "updated_at"
        ].replace(
            "Z",
            "+00:00"
        )

        pr_metadata = PRMetadata(
            pr_number=pr["number"],
            pr_title=pr["title"],
            pr_url=pr["html_url"],
            repo=repo,
            owner=owner,
            author=pr["user"]["login"],
            created_at=created_at,
            last_activity_at=updated_at,
            staleness_hours=0.0,
            reviewers=[],
            ci_status="pending",
            ci_error_message=None,
            labels=[
                label["name"]
                for label in pr.get(
                    "labels",
                    []
                )
            ],
            comment_count=pr[
                "comments"
            ],
            body=pr.get("body")
        )

        initial_state = WorkflowState(
            workflow_id=workflow_id,
            pr_url=pr_metadata.pr_url,
            pr_metadata=pr_metadata,
            status="running"
        )

        print(
            "\nSTARTING AI WORKFLOW..."
        )

        result = await graph.ainvoke(
            initial_state
        )

        print(
            "WORKFLOW COMPLETE"
        )

        return {
            "status":
                "workflow_triggered",

            "workflow_id":
                workflow_id,

            "decision":
                result.get(
                    "decision"
                )
        }

    print("====================\n")

    return {
        "status": "ignored",
        "event": event
    }