from langgraph.graph import StateGraph
from state.test_state import AppState
from ai.planner import planner_agent
from ai.executor import executor_agent
from ai.validator import validator_agent

def build_graph():
    graph = StateGraph(AppState)

    graph.add_node("planner", planner_agent)
    graph.add_node("executor", executor_agent)
    graph.add_node("validator", validator_agent)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "validator")

    return graph.compile()