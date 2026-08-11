import os
from state import GraphState
from utils.llm import call_llm


def insight_node(state: GraphState):
    data = state["aggregated"]

    prompt = f"""You are a senior malware analyst. Below is the complete analysis data for a suspicious file.
Your job is to produce a structured threat intelligence report based ONLY on the data provided.
Do not invent or assume anything beyond what is in the data.

---

## File Identity
- SHA256: {data.get("file_hash")}

## UPX Analysis
{data.get("upx")}

## FLOSS String Extraction
{data.get("floss")}

## Static PE Analysis
{data.get("static")}

## Dynamic / VirusTotal Analysis
{data.get("dynamic")}

## YARA Matches
{data.get("yara")}

---

Based on the above, produce a detailed threat intelligence report with the following sections:

### 1. Executive Summary
A short paragraph (3-5 sentences) summarizing what this file is, what it does, and how dangerous it is.

### 2. Threat Classification
- Malware Family / Label (e.g., specific family, or "Benign / Safe / Unknown" if no malicious indicators are found)
- Threat Type (trojan / backdoor / ransomware / benign / safe / etc.)
- Severity Level (Critical / High / Medium / Low / None) with justification (If the file shows no evidence of malicious behavior, has 0% or extremely low VirusTotal detection, and matches no malicious YARA rules, it must be classified as Benign / Safe with Low/None severity)

### 3. Technical Behavior
Describe in detail what the malware does based on the evidence:
- Network activity (C2, ports, protocols)
- Process activity (what processes it spawns or injects into)
- Persistence / evasion mechanisms
- Any anti-analysis behavior

### 4. Indicators of Compromise (IOCs) & Suspicious Artifacts
List all standard IOCs found in the data:
- Hashes (MD5, SHA1, SHA256)
- IPs / Domains / URLs
- File names / paths
- Mutex / Registry keys (if any)
- Ports

Additionally, deeply analyze the raw imports/exports and strings data provided above:
- **Critical Imports/Exports**: Extract the top 5-10 most suspicious or dangerous Windows APIs the malware uses (e.g., VirtualAllocEx, LoadLibrary, GetProcAddress, CreateRemoteThread, etc.) and explicitly explain what malicious capability they enable (e.g., Process Injection, Keylogging, Dynamic Loading).
- **Suspicious Strings**: Identify any highly suspicious strings (like registry keys, evasion commands, PDB paths, ransomware notes, or networking artifacts) and explain why they are dangerous.

### 5. Key Findings per Analysis Module
For each module, state the most important finding in 1-2 sentences:
- UPX
- FLOSS
- Static PE
- Dynamic / VT
- YARA

### 6. Risk Assessment
- Detection Rate
- Sandbox verdict vs AV verdict — any discrepancy?
- Confidence level in the analysis (High / Medium / Low) and why

### 7. Recommendations
What should a SOC analyst or incident responder do with this file?
List 3-5 concrete action items.

---

Rules:
- Be precise and technical
- Do not repeat the raw data, synthesize it
- If something is missing or unclear in the data, say so explicitly
- Use markdown formatting
- If the analysis data suggests the file is benign, clean, or has no malicious indicators, clearly identify it as Benign/Safe, set the severity to Low or None, and explain that no threat was detected."""

    insights = call_llm(prompt)

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/insights_report.md", "w", encoding="utf-8") as f:
        f.write(insights)

    print("insights")
    return {"insights": insights}
