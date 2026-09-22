from langgraph.graph import StateGraph, END
from agent.state import ReportState
from agent.nodes import (
    load_data_node,
    decide_analyses_node,
    trend_analysis_node,
    outlier_detection_node,
    forecast_node,
    generate_charts_node,
    write_narrative_node,
    build_pdf_node
)

def should_run_trends(state: ReportState):
    return "trends" in state["analyses_to_run"]

def should_run_outliers(state: ReportState):
    return "outliers" in state["analyses_to_run"]

def should_run_forecast(state: ReportState):
    return "forecast" in state["analyses_to_run"]

def build_graph():
    graph = StateGraph(ReportState)

    # Add all nodes
    graph.add_node("load_data", load_data_node)
    graph.add_node("decide_analyses", decide_analyses_node)
    graph.add_node("trend_analysis", trend_analysis_node)
    graph.add_node("outlier_detection", outlier_detection_node)
    graph.add_node("forecast", forecast_node)
    graph.add_node("generate_charts", generate_charts_node)
    graph.add_node("write_narrative", write_narrative_node)
    graph.add_node("build_pdf", build_pdf_node)

    # Define the flow
    graph.set_entry_point("load_data")
    graph.add_edge("load_data", "decide_analyses")

    # Conditional branching — agent decides what to run
    graph.add_conditional_edges(
        "decide_analyses",
        lambda state: state["analyses_to_run"],
        {
            "trends": "trend_analysis",
            "outliers": "outlier_detection",
            "forecast": "forecast",
        }
    )

    # All analysis nodes feed into chart generation
    graph.add_edge("trend_analysis", "generate_charts")
    graph.add_edge("outlier_detection", "generate_charts")
    graph.add_edge("forecast", "generate_charts")

    # Then narrative, then PDF
    graph.add_edge("generate_charts", "write_narrative")
    graph.add_edge("write_narrative", "build_pdf")
    graph.add_edge("build_pdf", END)

    return graph.compile()