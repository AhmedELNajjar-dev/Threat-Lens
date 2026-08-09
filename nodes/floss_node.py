import subprocess
import re
import json
import os
import platform
from config import BASE_DIR
from state import GraphState
from utils.llm import call_llm


def format_floss(data: dict) -> str:
    if "error" in data:
        return f"FLOSS string extraction failed: {data['error']}"
    
    total = data.get("total_strings", 0)
    urls = data.get("urls", [])
    ips = data.get("ips", [])
    commands = data.get("commands", [])
    other = data.get("other_strings", [])

    lines = [f"**Total Extracted Strings**: {total}\n"]

    if urls:
        lines.append("### Extracted URLs")
        lines.extend([f"- `{u}`" for u in urls])
        lines.append("")
    if ips:
        lines.append("### Extracted IP Addresses")
        lines.extend([f"- `{ip}`" for ip in ips])
        lines.append("")
    if commands:
        lines.append("### Command Execution Indicators")
        lines.extend([f"- `{cmd}`" for cmd in commands])
        lines.append("")
    if other:
        lines.append("### Other Notable Strings")
        lines.extend([f"- `{s}`" for s in other])
        lines.append("")

    if not (urls or ips or commands or other):
        lines.append("No prominent URLs, IPs, or command strings identified.")

    return "\n".join(lines)


def floss_node(state: GraphState):
    file_path = state["file_path"]

    try:
        if platform.system() == "Windows":
            floss_path = os.path.join(BASE_DIR, "floss64.exe")
        else:
            floss_path = os.path.join(BASE_DIR, "floss")
            
        result = subprocess.run(
            [floss_path, file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        lines = result.stdout.splitlines()

        urls = list(set([l for l in lines if "http" in l.lower()]))
        ips  = list(set([l for l in lines if re.search(r"\b\d{1,3}(\.\d{1,3}){3}\b", l)]))

        command_patterns = [r"\bcmd\b", r"\bpowershell\b", r"\bexec\b", r"\bsystem\b"]
        commands = list(set([
            l for l in lines
            if any(re.search(p, l, re.IGNORECASE) for p in command_patterns)
        ]))

        categorized  = set(urls + ips + commands)
        other_strings = list(set([l for l in lines if l not in categorized and l.strip()]))

        floss_result = {
            "total_strings": len(lines),
            "urls":          urls[:10],
            "ips":           ips[:10],
            "commands":      commands[:10],
            "other_strings": other_strings[:10]
        }
    except Exception as e:
        floss_result = {"error": str(e)}

    floss_result = {
        **floss_result,
        "llm_formatted": format_floss(floss_result)
    }
    print("floss")
    return {"floss_result": floss_result}
