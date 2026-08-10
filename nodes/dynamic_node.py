import json
from state import GraphState
from utils.llm import call_llm


def format_dynamic(data: dict) -> str:
    if not data:
        return "No dynamic analysis data available."
    
    lines = []
    lines.append(f"- **Detection Ratio**: {data.get('detection_ratio', 'N/A')}")
    lines.append(f"- **Suggested Threat Label**: `{data.get('threat_label', 'unknown')}`")
    tc_raw = data.get("threat_category", [])
    tc_list = [t.get("value", str(t)) if isinstance(t, dict) else str(t) for t in tc_raw]
    lines.append(f"- **Threat Categories**: {', '.join(tc_list) or 'None'}")
    lines.append(f"- **Reputation Score**: {data.get('reputation', 'N/A')}\n")

    verdicts = data.get("sandbox_verdicts", {})
    if verdicts:
        lines.append("### Sandbox Verdicts")
        for sb_name, sb_info in verdicts.items():
            if isinstance(sb_info, dict):
                confidence = sb_info.get('confidence')
                conf_str = f" ({confidence}% conf)" if confidence is not None else ""
                lines.append(f"- **{sb_name}**: `{sb_info.get('category', 'unknown')}`{conf_str}")
            else:
                lines.append(f"- **{sb_name}**: {sb_info}")
        lines.append("")

    raw_tags = data.get("behavior_tags", [])
    tags = [t.get("value", str(t)) if isinstance(t, dict) else str(t) for t in raw_tags]
    if tags:
        lines.append(f"### Behavior Tags\n`{', '.join(tags)}`\n")

    stats = data.get("av_stats", {})
    if stats:
        lines.append("### AV Engine Breakdown")
        for status, count in stats.items():
            lines.append(f"- **{status.capitalize()}**: {count}")
        lines.append("")

    return "\n".join(lines)


def dynamic_node(state: GraphState):
    vt = state.get("vt_data", {})

    try:
        attrs = vt["data"]["attributes"]

        stats           = attrs.get("last_analysis_stats", {})
        total           = sum(v for k, v in stats.items() if k != "type-unsupported")
        malicious_count = stats.get("malicious", 0)
        detection_ratio = round(malicious_count / total * 100, 1) if total else 0

        dynamic_analysis = {
            "sandbox_verdicts": attrs.get("sandbox_verdicts", {}),
            "av_stats":         stats,
            "detection_ratio":  f"{malicious_count}/{total} ({detection_ratio}%)",
            "crowdsourced_ai":  attrs.get("crowdsourced_ai_results", []),
            "crowdsourced_ids": attrs.get("crowdsourced_ids_results", []),
            "sigma":            attrs.get("sigma_analysis_results", []),
            "threat_label": (
                attrs
                .get("popular_threat_classification", {})
                .get("suggested_threat_label", "unknown")
            ),
            "threat_category": (
                attrs
                .get("popular_threat_classification", {})
                .get("popular_threat_category", [])
            ),
            "reputation":    attrs.get("reputation"),
            "total_votes":   attrs.get("total_votes", {}),
            "behavior_tags": attrs.get("tags", []),
            "network":       attrs.get("network_infrastructure", {}),
        }

    except KeyError as e:
        print(f"[dynamic_node] KeyError: {e}")
        dynamic_analysis = {}
    except Exception as e:
        print(f"[dynamic_node] Error: {e}")
        dynamic_analysis = {}

    dynamic_analysis = {
        **dynamic_analysis,
        "llm_formatted": format_dynamic(dynamic_analysis)
    }
    print("dynamic")
    return {"dynamic_analysis": dynamic_analysis}
