from langgraph.graph import StateGraph, END

from schemas.schemas import (
    WorkflowState,
    PRMetadata
)

from agents.memory import (
    retrieve,
    persist
)

from agents.pr_analysis import (
    run_pr_analysis
)

from agents.communication import (
    run_communication_analysis
)

from agents.priority import (
    run_priority_analysis
)

from agents.research import (
    run_research_agent
)

from agents.reflection import (
    run_reflection_agent
)

from agents.planner import (
    run_planner_agent
)

from agents.notification import (
    run_notification_agent
)

from agents.summary import (
    run_summary_agent
)


#
# MEMORY RETRIEVE NODE
#
async def memory_retrieve_node(
    state: WorkflowState
):

    if state.pr_metadata:

        incidents = retrieve(
            pr_author=state.pr_metadata.author,
            repo=state.pr_metadata.repo
        )

        state.past_incidents = incidents

    return state


#
# ANALYSIS NODE
#
async def analysis_node(
    state: WorkflowState
):

    # If simulated PR metadata already exists,
    # skip GitHub API fetching.

    if state.pr_metadata:

        from schemas.schemas import AgentResult

        simulated_result = AgentResult(
            agent_name="pr_analysis",
            status="success",
            findings=state.pr_metadata.model_dump(),
            confidence=1.0,
            recommended_action=None,
            duration_ms=0,
            tokens_used=0,
            error_message=None
        )

        state.agent_results.append(
            simulated_result
        )

        return state

    return state


#
# COMMUNICATION NODE
#
async def communication_node(
    state: WorkflowState
):

    comments = ""

    if state.pr_metadata:
        comments = state.pr_metadata.body or ""

    result = await run_communication_analysis(
        workflow_id=state.workflow_id,
        comments=comments
    )

    state.agent_results.append(result)

    return state


#
# PRIORITY NODE
#
async def priority_node(
    state: WorkflowState
):

    communication_data = {}

    for result in state.agent_results:
        if result.agent_name == "communication":
            communication_data = result.findings

    result = await run_priority_analysis(
        workflow_id=state.workflow_id,
        pr_data=state.pr_metadata,
        communication_data=communication_data,
        past_incident_count=len(
            state.past_incidents
        )
    )

    state.agent_results.append(result)

    return state


#
# RESEARCH NODE
#
async def research_node(
    state: WorkflowState
):

    result = await run_research_agent(
        workflow_id=state.workflow_id,
        pr_metadata=state.pr_metadata
    )

    state.agent_results.append(result)

    return state


#
# REFLECTION NODE
#
async def reflection_node(
    state: WorkflowState
):

    result = await run_reflection_agent(
        workflow_id=state.workflow_id,
        pr_number=state.pr_metadata.pr_number,
        repo=state.pr_metadata.repo,
        agent_results=state.agent_results
    )

    state.agent_results.append(result)

    state.confidence = (
        result.findings.get(
            "confidence",
            "MEDIUM"
        ).lower()
    )

    return state


#
# PLANNER NODE
#
async def planner_node(
    state: WorkflowState
):

    result = await run_planner_agent(
        workflow_id=state.workflow_id,
        past_incidents=state.past_incidents,
        agent_results=state.agent_results
    )

    state.agent_results.append(result)

    state.decision = result.findings.get(
        "decision"
    )

    return state


#
# NOTIFICATION NODE
#
async def notification_node(
    state: WorkflowState
):

    reflection_reasoning = ""

    for result in state.agent_results:
        if result.agent_name == "reflection":
            reflection_reasoning = (
                result.findings.get(
                    "confidence_reasoning",
                    ""
                )
            )

    result = await run_notification_agent(
        workflow_id=state.workflow_id,
        decision=state.decision,
        pr_metadata=state.pr_metadata,
        reflection_reasoning=reflection_reasoning
    )

    state.agent_results.append(result)

    state.action_taken = result.findings

    return state


#
# SUMMARY NODE
#
async def summary_node(
    state: WorkflowState
):

    result = await run_summary_agent(
        workflow_id=state.workflow_id,
        pr_metadata=state.pr_metadata,
        agent_results=state.agent_results,
        decision=state.decision,
        action_taken=state.action_taken
    )

    state.agent_results.append(result)

    state.summary = result.findings.get(
        "report_markdown",
        ""
    )

    return state


#
# MEMORY PERSIST NODE
#
async def memory_persist_node(
    state: WorkflowState
):

    # MARK WORKFLOW COMPLETE
    # BEFORE PERSISTING
    state.status = "completed"

    persist(state)

    return state


#
# BUILD GRAPH
#
workflow = StateGraph(
    WorkflowState
)

workflow.add_node(
    "memory_retrieve",
    memory_retrieve_node
)

workflow.add_node(
    "analysis",
    analysis_node
)

workflow.add_node(
    "communication",
    communication_node
)

workflow.add_node(
    "priority",
    priority_node
)

workflow.add_node(
    "research",
    research_node
)

workflow.add_node(
    "reflection",
    reflection_node
)

workflow.add_node(
    "planner",
    planner_node
)

workflow.add_node(
    "notification",
    notification_node
)

workflow.add_node(
    "summary",
    summary_node
)

workflow.add_node(
    "memory_persist",
    memory_persist_node
)

#
# ENTRY
#
workflow.set_entry_point(
    "memory_retrieve"
)

#
# EDGES
#
workflow.add_edge(
    "memory_retrieve",
    "analysis"
)

workflow.add_edge(
    "analysis",
    "communication"
)

workflow.add_edge(
    "communication",
    "priority"
)

workflow.add_edge(
    "priority",
    "research"
)

workflow.add_edge(
    "research",
    "reflection"
)

workflow.add_edge(
    "reflection",
    "planner"
)

workflow.add_edge(
    "planner",
    "notification"
)

workflow.add_edge(
    "notification",
    "summary"
)

workflow.add_edge(
    "summary",
    "memory_persist"
)

workflow.add_edge(
    "memory_persist",
    END
)

graph = workflow.compile()