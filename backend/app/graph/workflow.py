from langgraph.graph import (
    END,
    StateGraph,
)

from app.graph.nodes import (
    llm_node,
    route_after_llm,
    tool_node,
)

from app.graph.state import AgentState


def build_graph():

    graph = StateGraph(
        AgentState
    )

    graph.add_node(
        "llm",
        llm_node,
    )

    graph.add_node(
        "tools",
        tool_node,
    )

    graph.set_entry_point(
        "llm"
    )

    graph.add_conditional_edges(
        "llm",
        route_after_llm,
        {
            "tools": "tools",
            "end": END,
        },
    )

    graph.add_edge(
        "tools",
        "llm",
    )

    return graph.compile()