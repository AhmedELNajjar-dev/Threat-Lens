import json
import os
from state import GraphState


def aggregation_node(state: GraphState):
    aggregated = {
        "file_hash": state.get("file_hash"),
        "upx":       state.get("upx_result",      {}).get("llm_summary"),
        "floss":     state.get("floss_result",     {}).get("llm_formatted"),
        "static":    state.get("static_analysis",  {}).get("llm_formatted"),
        "dynamic":   state.get("dynamic_analysis", {}).get("llm_formatted"),
        "yara":      state.get("yara_result",      {}).get("llm_formatted"),
    }

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/analysis.json", "w", encoding="utf-8") as f:
        json.dump(aggregated, f, indent=2, ensure_ascii=False)

    print("agg")
    return {"aggregated": aggregated}
