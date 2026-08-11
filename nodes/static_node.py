import json
from state import GraphState
from utils.llm import call_llm


def format_static(data: dict) -> str:
    if not data:
        return "No static PE analysis data available."
    
    lines = []
    lines.append(f"- **File Type**: {data.get('file_type', 'N/A')}")
    lines.append(f"- **File Size**: {data.get('size', 'N/A')} bytes")
    lines.append(f"- **Machine Type**: {data.get('machine_type', 'N/A')}")
    lines.append(f"- **Entry Point**: {data.get('entry_point', 'N/A')}")
    lines.append(f"- **Imphash**: `{data.get('imphash', 'N/A')}`")
    lines.append(f"- **SSDEEP**: `{data.get('ssdeep', 'N/A')}`")
    lines.append(f"- **MD5**: `{data.get('md5', 'N/A')}`")
    lines.append(f"- **SHA1**: `{data.get('sha1', 'N/A')}`")
    lines.append(f"- **SHA256**: `{data.get('sha256', 'N/A')}`\n")

    entropy_values = data.get("entropy_values", [])
    if entropy_values:
        lines.append("### PE Sections & Entropy")
        for s in entropy_values:
            flag = "⚠️ (HIGH ENTROPY)" if s.get("flagged") else ""
            lines.append(f"- Section `{s.get('section')}`: Entropy `{s.get('entropy')}` {flag}")
        lines.append("")

    die = data.get("detectiteasy", [])
    if die:
        lines.append("### Detect It Easy / Tool Identifiers")
        for item in die:
            if isinstance(item, dict):
                name = item.get('name', '')
                version = item.get('version', '')
                combined = f"{name} {version}".strip()
                lines.append(f"- {combined}")
            else:
                lines.append(f"- {item}")
        lines.append("")

    packers = data.get("packers", {})
    if packers:
        lines.append("### Detected Packers")
        for tool, details in packers.items():
            lines.append(f"- **{tool}**: `{details}`")
        lines.append("")

    imports = data.get("imports", [])
    if imports:
        # Dictionary of suspicious/critical Windows APIs commonly used by malware
        suspicious_apis = {
            "LoadLibraryA": "Dynamic DLL loading",
            "LoadLibraryW": "Dynamic DLL loading",
            "GetProcAddress": "Dynamic API resolution",
            "VirtualAlloc": "Memory allocation (often for unpacking)",
            "VirtualAllocEx": "Process injection",
            "WriteProcessMemory": "Process injection",
            "CreateRemoteThread": "Process injection",
            "CreateProcessA": "Spawning processes",
            "CreateProcessW": "Spawning processes",
            "URLDownloadToFileA": "Downloading payloads",
            "URLDownloadToFileW": "Downloading payloads",
            "InternetOpenA": "Network comms / C2",
            "InternetOpenW": "Network comms / C2",
            "RegSetValueExA": "Registry persistence",
            "RegCreateKeyExA": "Registry persistence",
            "SetWindowsHookExA": "Keylogging / Hooking",
            "SetWindowsHookExW": "Keylogging / Hooking",
            "IsDebuggerPresent": "Anti-debugging",
            "CheckRemoteDebuggerPresent": "Anti-debugging",
            "Sleep": "Sandbox evasion (delay)",
            "CryptAcquireContextA": "Cryptography / Encryption",
            "WinExec": "Executing commands",
            "ShellExecuteA": "Executing commands"
        }

        lines.append(f"### Import Libraries ({len(imports)} libraries)")
        for imp in imports[:10]:
            lib = imp.get("library_name", "Unknown")
            funcs = imp.get("imported_functions", [])
            lines.append(f"- **{lib}** ({len(funcs)} functions):")
            
            # Display up to 20 functions, highlight the suspicious ones
            func_display = []
            for f in funcs[:20]:
                if f in suspicious_apis:
                    func_display.append(f"`{f}` ⚠️ *( {suspicious_apis[f]} )*")
                else:
                    func_display.append(f"`{f}`")
            
            if func_display:
                lines.append("  " + ", ".join(func_display) + (", ..." if len(funcs) > 20 else ""))
                
        if len(imports) > 10:
            lines.append(f"- ... and {len(imports) - 10} more libraries")
        lines.append("")

    exports = data.get("exports", [])
    if exports:
        suspicious_exports = {
            "DllRegisterServer": "COM Hijacking / regsvr32 execution",
            "DllUnregisterServer": "COM Hijacking",
            "DllInstall": "COM Hijacking",
            "ServiceMain": "Windows Service persistence",
            "SvchostPushServiceGlobals": "svchost.exe persistence",
            "MiniDump": "Memory dumping (LSASS credential theft)",
            "Install": "Potential malware installer",
            "Uninstall": "Potential malware uninstaller",
            "Start": "Generic start execution",
            "Run": "Generic run execution",
            "Execute": "Generic payload execution",
            "Payload": "Explicit payload export",
            "Inject": "Code injection",
            "Loader": "Malware loader",
            "Hook": "Keylogging / API hooking"
        }

        lines.append(f"### Exported Functions ({len(exports)})")
        
        # Display up to 20 exports, highlight the suspicious ones
        exp_display = []
        for exp in exports[:20]:
            if exp in suspicious_exports:
                exp_display.append(f"`{exp}` ⚠️ *( {suspicious_exports[exp]} )*")
            else:
                exp_display.append(f"`{exp}`")
                
        if exp_display:
            lines.append("- " + ", ".join(exp_display) + (", ..." if len(exports) > 20 else ""))
        
        lines.append("")

    return "\n".join(lines)


def static_node(state: GraphState):
    vt = state.get("vt_data", {})

    try:
        attrs = vt["data"]["attributes"]
        pe    = attrs.get("pe_info", {})

        sections = pe.get("sections", [])
        imports  = pe.get("import_list", [])
        exports  = pe.get("exports", {}).get("exported_functions", [])

        entropy_values = [
            {
                "section": s.get("name"),
                "entropy": s.get("entropy"),
                "flagged": (s.get("entropy") or 0) >= 7.0
            }
            for s in sections
        ]

        detectiteasy = attrs.get("detectiteasy", {})
        packers      = attrs.get("packers", {})

        static_analysis = {
            "sections":       sections,
            "imports":        imports,
            "exports":        exports,
            "entropy_values": entropy_values,
            "timestamp":      pe.get("timestamp"),
            "entry_point":    pe.get("entry_point"),
            "machine_type":   pe.get("machine_type"),
            "imphash":        pe.get("imphash"),
            "rich_pe_hash":   pe.get("rich_pe_header_hash"),
            "resources":      pe.get("resource_details", []),
            "file_type":      attrs.get("type_description"),
            "magic":          attrs.get("magic"),
            "trid":           attrs.get("trid", []),
            "detectiteasy":   detectiteasy.get("values", []),
            "packers":        packers,
            "tags":           attrs.get("tags", []),
            "known_names":    attrs.get("names", []),
            "md5":            attrs.get("md5"),
            "sha1":           attrs.get("sha1"),
            "sha256":         attrs.get("sha256"),
            "ssdeep":         attrs.get("ssdeep"),
            "authentihash":   attrs.get("authentihash"),
            "size":           attrs.get("size"),
        }

    except KeyError as e:
        print(f"[static_node] KeyError — missing key: {e}")
        static_analysis = {}
    except Exception as e:
        print(f"[static_node] Unexpected error: {e}")
        static_analysis = {}

    static_analysis = {
        **static_analysis,
        "llm_formatted": format_static(static_analysis)
    }
    print("static")
    return {"static_analysis": static_analysis}
