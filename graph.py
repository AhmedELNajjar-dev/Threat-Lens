from langgraph.graph import StateGraph, END

from state import GraphState
from nodes.hash_node             import hash_node
from nodes.upx_node              import upx_check_node
from nodes.floss_node            import floss_node
from nodes.vt_node               import vt_node
from nodes.static_node           import static_node
from nodes.dynamic_node          import dynamic_node
from nodes.yara_node             import yara_node
from nodes.aggregation_node      import aggregation_node
from nodes.insight_node          import insight_node
from nodes.summary_report_node   import summary_report_node
from nodes.render_report_html_node import render_report_html_node


def input_node(state: GraphState):
    return state


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("input",             input_node)
    builder.add_node("hash",              hash_node)
    builder.add_node("upx",               upx_check_node)
    builder.add_node("floss",             floss_node)
    builder.add_node("vt",                vt_node)
    builder.add_node("static",            static_node)
    builder.add_node("dynamic",           dynamic_node)
    builder.add_node("yara",              yara_node)
    builder.add_node("agg",               aggregation_node)
    builder.add_node("insight",           insight_node)
    builder.add_node("summary_report",    summary_report_node)
    builder.add_node("render_report_html", render_report_html_node)

    builder.set_entry_point("input")

    builder.add_edge("input", "hash")
    builder.add_edge("hash", "vt")
    builder.add_edge("vt", "static")
    builder.add_edge("static", "dynamic")
    builder.add_edge("dynamic", "upx")
    builder.add_edge("upx", "floss")
    builder.add_edge("floss", "yara")
    builder.add_edge("yara", "agg")

    builder.add_edge("agg",     "insight")
    builder.add_edge("insight", "summary_report")
    builder.add_edge("agg",     "render_report_html")

    builder.add_edge("summary_report",    END)
    builder.add_edge("render_report_html", END)

    return builder.compile()


graph = build_graph()
