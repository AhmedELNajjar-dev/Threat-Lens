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
    suspicious = data.get("suspicious", [])
    urls = data.get("urls", [])
    ips = data.get("ips", [])
    commands = data.get("commands", [])
    other = data.get("other_strings", [])

    lines = [f"**Total Extracted Strings**: {total}\n"]

    if suspicious:
        lines.append("### ⚠️ Highly Suspicious Strings")
        lines.extend([f"- {s}" for s in suspicious])
        lines.append("")
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

    if not (urls or ips or commands or other or suspicious):
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

        suspicious_dict = {
            r"Software\\Microsoft\\Windows\\CurrentVersion\\Run": "Registry persistence (Run key)",
            r"SeDebugPrivilege": "Privilege escalation / Code injection",
            r"Failed to create service": "Service installation (persistence)",
            r"vssadmin.*delete shadows": "Ransomware (Deleting shadow copies)",
            r"WSAStartup": "Network socket initialization",
            r"CreateRemoteThread": "Process injection API string",
            r"LoadLibrary": "Dynamic DLL loading string",
            r"\.pdb$": "Debug symbol path (Compiler artifact)",
            r"VirtualAlloc": "Memory allocation string",
            r"stratum\+tcp": "Cryptocurrency miner protocol"
        }

        suspicious_matches = []
        for l in lines:
            for pat, hint in suspicious_dict.items():
                if re.search(pat, l, re.IGNORECASE):
                    suspicious_matches.append(f"`{l.strip()}` ⚠️ *( {hint} )*")
                    
        suspicious_matches = list(set(suspicious_matches))

        categorized  = set(urls + ips + commands + [s.split("`")[1] for s in suspicious_matches if "`" in s])
        other_strings = list(set([l for l in lines if l not in categorized and l.strip()]))

        floss_result = {
            "total_strings": len(lines),
            "suspicious":    suspicious_matches[:15],
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
