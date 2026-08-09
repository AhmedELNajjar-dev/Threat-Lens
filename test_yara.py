import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from utils.yara_loader import load_clean_rules

rules = load_clean_rules()
print(f"Total rules loaded: {len(list(rules)) if hasattr(rules, '__iter__') else 'Unknown'}")

matches = rules.match(os.path.join(os.path.dirname(__file__), "eicar.com"))
print("Matches:")
for m in matches:
    print(f"- {m.rule} (namespace: {m.namespace})")
