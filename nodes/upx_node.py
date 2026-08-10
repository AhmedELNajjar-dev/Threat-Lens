import subprocess
import json
import os
import platform
from config import BASE_DIR
from state import GraphState
from utils.llm import call_llm


def format_upx(data: dict) -> str:
    if "error" in data:
        return f"UPX scan failed: {data['error']}"
    if data.get("packed", False):
        return "The sample is packed with UPX executable compression, indicating intentional binary obfuscation and payload packing."
    return "The sample is not packed with UPX executable compression."


def upx_check_node(state: GraphState):
    file_path = state["file_path"]

    try:
        if platform.system() == "Windows":
            upx_path = os.path.join(BASE_DIR, "upx.exe")
        else:
            upx_path = "upx"
            
        result = subprocess.run(
            [upx_path, "-t", file_path],
            capture_output=True,
            text=True
        )
        packed = "packed" in result.stdout.lower()
        upx_result = {
            "packed": packed,
            "raw_output": result.stdout
        }
    except Exception as e:
        upx_result = {"error": str(e)}

    upx_result = {
        **upx_result,
        "llm_summary": format_upx(upx_result)
    }
    print("upx")
    return {"upx_result": upx_result}
