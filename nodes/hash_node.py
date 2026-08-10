import hashlib
from state import GraphState


def hash_node(state: GraphState):
    file_path = state["file_path"]

    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)

    print("hash")
    file_hash = sha256.hexdigest()
    return {"file_hash": file_hash}
