import requests
from state import GraphState
from config import VT_API_KEY


def vt_node(state: GraphState):
    file_hash = state["file_hash"]

    url     = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VT_API_KEY}

    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        vt_data = res.json()
    else:
        vt_data = {"error": res.status_code}

    print("vt")
    return {"vt_data": vt_data}
