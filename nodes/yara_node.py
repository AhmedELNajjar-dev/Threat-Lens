import json
from state import GraphState
from utils.llm import call_llm
from utils.yara_loader import load_clean_rules

YARA_RULES = load_clean_rules()


def format_yara(data: dict) -> str:
    if "error" in data:
        return f"YARA scan failed: {data['error']}"
    
    count = data.get("match_count", 0)
    severity = data.get("severity", "none").upper()
    categories = data.get("matched_categories", [])
    rules = data.get("matched_rules", [])

    lines = []
    lines.append(f"- **Match Count**: {count}")
    lines.append(f"- **Calculated Severity**: `{severity}`")
    cat_list = [str(c) for c in categories]
    lines.append(f"- **Categories Hit**: {', '.join(cat_list) if cat_list else 'None'}\n")

    if rules:
        lines.append("### Matched YARA Rules")
        for r in rules:
            rule_name = r.get("rule")
            ns = r.get("namespace")
            tags_list = [str(t) for t in r.get("tags", [])]
            tags = ", ".join(tags_list)
            lines.append(f"- **{rule_name}** (Category: `{ns}`" + (f", Tags: `{tags}`" if tags else "") + ")")
        lines.append("")
    else:
        lines.append("No YARA rules matched for this file.")

    return "\n".join(lines)


def yara_node(state: GraphState):
    file_path = state["file_path"]

    try:
        matches    = YARA_RULES.match(file_path)
        results    = []
        namespaces = set()

        for m in matches:
            namespaces.add(m.namespace.split("_")[0])
            results.append({
                "rule":      m.rule,
                "namespace": m.namespace.split("_")[0],
                "tags":      m.tags,
                "meta":      dict(m.meta)
            })

        if "malware" in namespaces:
            severity = "high"
        elif "webshells" in namespaces:
            severity = "medium"
        elif "packers" in namespaces:
            severity = "low"  # Benign files can also be packed
        elif len(results) > 0:
            severity = "low"
        else:
            severity = "none"

        yara_result = {
            "match_count":        len(results),
            "severity":           severity,
            "matched_categories": list(namespaces),
            "matched_rules":      results
        }

    except Exception as e:
        yara_result = {"error": str(e)}

    yara_result = {
        **yara_result,
        "llm_formatted": format_yara(yara_result)
    }
    print("yara")
    return {"yara_result": yara_result}
