import sys
import os
from graph import graph

if __name__ == "__main__":
    targets = []
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isdir(arg):
            for root, _, files in os.walk(arg):
                for f in files:
                    targets.append(os.path.join(root, f))
        elif os.path.isfile(arg):
            targets.append(arg)
        else:
            print(f"[!] Target not found: {arg}")
            sys.exit(1)
    else:
        default_file = "Lab09-02.exe"
        if os.path.exists(default_file):
            targets.append(default_file)
        else:
            print("[!] Usage: python main.py <file_or_directory_path>")
            sys.exit(1)

    print(f"[+] Found {len(targets)} sample(s) for analysis.")
    for idx, target in enumerate(targets, 1):
        print(f"\n[{idx}/{len(targets)}] Analyzing: {target}...")
        try:
            result = graph.invoke({"file_path": target})
            print(f"[+] Analysis complete for {target}. Hash: {result.get('file_hash')}")
        except Exception as e:
            print(f"[!] Error analyzing {target}: {e}")
