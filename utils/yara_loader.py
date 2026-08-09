# import os
# import yara
# from config import YARA_RULES_PATH


# def load_clean_rules(base_path: str = YARA_RULES_PATH):
#     rule_files = {}

#     for namespace in ["malware", "packers", "webshells"]:
#         folder = os.path.join(base_path, namespace)

#         for root, _, files in os.walk(folder):
#             for file in files:
#                 if file.endswith(".yar") or file.endswith(".yara"):
#                     full_path = os.path.join(root, file)

#                     try:
#                         yara.compile(filepath=full_path)
#                         key = f"{namespace}_{file}"
#                         rule_files[key] = full_path

#                     except Exception as e:
#                         print(f"[!] Skipping bad rule: {file} -> {e}")

#     return yara.compile(filepaths=rule_files)



import os
import yara  # type: ignore
import streamlit as st
from config import YARA_RULES_PATH

@st.cache_resource
def load_clean_rules(base_path: str = YARA_RULES_PATH):
    rule_files = {}
    common_path = os.path.join(base_path, "malware", "000_common_rules.yar")
    has_common = os.path.exists(common_path)

    for namespace in ["malware", "packers", "webshells"]:
        folder = os.path.join(base_path, namespace)
        if not os.path.exists(folder):
            continue

        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".yar") or file.endswith(".yara"):
                    full_path = os.path.join(root, file)

                    try:
                        yara.compile(filepath=full_path)
                        key = f"{namespace}_{file}"
                        rule_files[key] = full_path
                    except Exception as e:
                        if has_common and full_path != common_path:
                            try:
                                yara.compile(filepaths={"common": common_path, "target": full_path})
                                key = f"{namespace}_{file}"
                                rule_files[key] = full_path
                            except Exception as ex:
                                print(f"[!] Skipping bad rule: {file} -> {ex}")
                        else:
                            print(f"[!] Skipping bad rule: {file} -> {e}")

    compiled_rules = yara.compile(filepaths=rule_files)
    print(f"[+] YARA rules loaded: {len(rule_files)} files compiled")
    return compiled_rules