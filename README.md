# 🛡 ThreatLens

> ThreatLens — Automated Malware Intelligence Pipeline. Upload a binary, get a full threat report: SHA256, UPX packing detection, FLOSS string extraction, VirusTotal lookup, static PE analysis, dynamic sandbox results, YARA rule matching, and an AI-synthesized threat intelligence report — all in one click, powered by LangGraph + Groq.

---

## 📁 Project Structure

```
ThreatLens/
│
├── app.py                         # Streamlit web interface
├── config.py                      # API keys & shared constants
├── state.py                       # GraphState TypedDict
├── graph.py                       # Graph builder & compiler
├── main.py                        # CLI entry point
├── requirements.txt
│
├── nodes/
│   ├── hash_node.py               # SHA256 hashing
│   ├── upx_node.py                # UPX packer detection
│   ├── floss_node.py              # FLOSS string extraction
│   ├── vt_node.py                 # VirusTotal API lookup
│   ├── static_node.py             # Static PE analysis
│   ├── dynamic_node.py            # Dynamic / sandbox analysis
│   ├── yara_node.py               # YARA rule matching
│   ├── aggregation_node.py        # Fan-in aggregator
│   ├── insight_node.py            # LLM threat intelligence report
│   ├── summary_report_node.py     # LLM → premium HTML summary
│   └── render_report_html_node.py # Markdown → full HTML report
│
├── utils/
│   ├── llm.py                     # Groq client + call_llm()
│   └── yara_loader.py             # YARA rules loader
│
├── rules/                         # YARA rule files (see setup below)
│   ├── malware/
│   ├── packers/
│   └── webshells/
│
└── outputs/                       # Generated reports (auto-created)
    ├── analysis.json
    ├── insights_report.md
    ├── summary_report.html
    └── full_report.html
```

---

## ⚙️ Pipeline Flow

```
input ──┬──► hash ──► vt ──┬──► static ──┐
        │                  └──► dynamic ──┤
        ├──► upx ──► floss ──────────────┤
        │                                ├──► agg ──► insight ──► summary_report
        └──► yara ───────────────────────┘         └──────────► render_report_html
```

---

## 🚀 Installation & Setup

### 1. Clone the repo

```bash
git clone https://github.com/Ahmedsalah-28/ThreatLens.git
cd ThreatLens
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install external tools

- **UPX** — download from https://upx.github.io and add to PATH
- **FLOSS** — download `floss64.exe` from https://github.com/mandiant/flare-floss/releases and place it in the project root or add to PATH

### 4. Download YARA Rules

The pipeline uses community YARA rules. Clone them into the `rules/` folder:

```bash
git clone https://github.com/Yara-Rules/rules.git rules
```

> Repo: https://github.com/Yara-Rules/rules

After cloning, the `rules/` folder should contain at minimum:

```
rules/
├── malware/
├── packers/
└── webshells/
```

### 5. Configure API keys

Edit `config.py` and fill in your keys:

```python
GROQ_API_KEY    = "your_groq_api_key"
VT_API_KEY      = "your_virustotal_api_key"
YARA_RULES_PATH = "rules"
```

- **Groq API key** → https://console.groq.com
- **VirusTotal API key** → https://www.virustotal.com/gui/my-apikey

---

## ▶️ Usage

### Run the Streamlit web interface

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`, upload a binary, and click **Run Analysis**.

### Run from CLI

```bash
python main.py
```

> Edit the `file_path` inside `main.py` to point to your sample.

---

## 📊 Output Reports

After analysis, two HTML reports are generated inside `outputs/`:

| File | Description |
|---|---|
| `summary_report.html` | AI-generated premium interactive dashboard |
| `full_report.html` | Full technical report with all module results |
| `insights_report.md` | Raw markdown threat intelligence report |
| `analysis.json` | Aggregated raw data from all modules |

---

## ⚠️ Disclaimer

This tool is intended for **educational and research purposes only**.  
Always analyze malware in an **isolated environment** (VM / sandbox).  
Never run suspicious binaries on your host machine.
