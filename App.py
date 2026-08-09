import streamlit as st
import os
import tempfile
import base64
from pathlib import Path

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="ThreatLens | Automated Threat Intelligence",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg:         #05070e;
    --surface:    #0a0e1a;
    --card:       #0e1322;
    --card-hover: #13192c;
    --border:     #1b233a;
    --border2:    #2a3556;
    --accent:     #00f3ff;
    --accent-glow: rgba(0, 243, 255, 0.2);
    --accent2:    #9d4edd;
    --danger:     #ff2a6d;
    --success:    #00ff9d;
    --warning:    #ffb703;
    --text:       #e2e8f0;
    --muted:      #64748b;
    --mono:       'Share Tech Mono', monospace;
    --font-heading: 'Rajdhani', sans-serif;
    --font-body: 'Inter', sans-serif;
}

/* ── Reset & Base Layout ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 90% 60% at 50% -10%, rgba(0, 243, 255, 0.08) 0%, transparent 70%),
        radial-gradient(ellipse 70% 50% at 85% 85%, rgba(157, 78, 221, 0.06) 0%, transparent 65%),
        radial-gradient(circle at 15% 50%, rgba(0, 255, 157, 0.03) 0%, transparent 50%),
        var(--bg) !important;
}

.main .block-container {
    padding: 2rem 2rem 4rem !important;
    max-width: 1200px !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ── Hero Section ── */
.hero-wrap {
    text-align: center !important;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
    margin-bottom: 2rem;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 243, 255, 0.06);
    border: 1px solid rgba(0, 243, 255, 0.25);
    color: var(--accent);
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 6px 20px;
    border-radius: 20px;
    margin-bottom: 1.2rem;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.1);
}
.hero-tag::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 8px var(--accent);
}
.hero-title {
    font-family: var(--font-heading);
    font-size: clamp(3.2rem, 6vw, 5rem);
    font-weight: 700;
    line-height: 1.0;
    letter-spacing: 1px;
    background: linear-gradient(135deg, #ffffff 10%, var(--accent) 55%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
    filter: drop-shadow(0 0 25px rgba(0, 243, 255, 0.15));
}
.hero-sub {
    font-size: 15px !important;
    color: #94a3b8 !important;
    font-weight: 400 !important;
    letter-spacing: 0.2px !important;
    max-width: 700px !important;
    margin: 0 auto 2rem !important;
    line-height: 1.6 !important;
    text-align: center !important;
    text-align-last: center !important;
    display: block !important;
    width: 100% !important;
}
.hero-line {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, var(--border2) 30%, var(--border2) 70%, transparent 100%);
    margin-top: 1rem;
    position: relative;
}
.hero-line::after {
    content: '◈';
    position: absolute;
    left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    color: var(--accent);
    font-size: 12px;
    background: var(--bg);
    padding: 0 12px;
}

/* ── Section Card Container ── */
.cyber-card {
    background: rgba(14, 19, 34, 0.75);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.8rem 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    position: relative;
}
.cyber-card::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--accent2), transparent);
}
.card-label {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 3.5px;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.card-label::before {
    content: '';
    width: 12px; height: 2px;
    background: var(--accent);
    box-shadow: 0 0 6px var(--accent);
}

/* ── Streamlit Radio (Scan Mode Selector) Override ── */
[data-testid="stRadio"] {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 8px !important;
    padding: 6px !important;
    margin-bottom: 1.2rem !important;
}
[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 8px !important;
}
[data-testid="stRadio"] label {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 6px !important;
    padding: 10px 22px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    color: var(--muted) !important;
    font-family: var(--font-heading) !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
[data-testid="stRadio"] label:hover {
    color: var(--text) !important;
    background: rgba(255, 255, 255, 0.03) !important;
}
[data-testid="stRadio"] label[data-checked="true"] {
    background: rgba(0, 243, 255, 0.08) !important;
    border-color: rgba(0, 243, 255, 0.3) !important;
    color: var(--accent) !important;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.12) !important;
}
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
    font-size: 14px !important;
    font-family: var(--font-heading) !important;
    font-weight: 600 !important;
}

/* ── Streamlit File Uploader Override ── */
[data-testid="stFileUploader"] > div {
    background: rgba(10, 14, 26, 0.6) !important;
    border: 1.5px dashed var(--border2) !important;
    border-radius: 8px !important;
    padding: 2.2rem 1.5rem !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: var(--accent) !important;
    background: rgba(0, 243, 255, 0.04) !important;
    box-shadow: 0 0 20px rgba(0, 243, 255, 0.08) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] p {
    font-family: var(--mono) !important;
    font-size: 13px !important;
    color: var(--muted) !important;
}
[data-testid="stFileUploader"] button {
    background: rgba(0, 243, 255, 0.08) !important;
    border: 1px solid rgba(0, 243, 255, 0.3) !important;
    color: var(--accent) !important;
    font-family: var(--font-heading) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    padding: 6px 18px !important;
    transition: all 0.2s !important;
}
[data-testid="stFileUploader"] button:hover {
    background: var(--accent) !important;
    color: #000 !important;
    box-shadow: 0 0 15px var(--accent) !important;
}

/* ── Streamlit Text Input Override ── */
[data-testid="stTextInput"] input {
    background: rgba(10, 14, 26, 0.8) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 6px !important;
    color: var(--accent) !important;
    font-family: var(--mono) !important;
    font-size: 13px !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.2) !important;
}

/* ── Action Buttons Styling ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(0, 243, 255, 0.12) 0%, rgba(157, 78, 221, 0.12) 100%) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: var(--font-heading) !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2rem !important;
    border-radius: 6px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.1) !important;
}
.stButton > button:hover:not(:disabled) {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #000 !important;
    box-shadow: 0 0 25px rgba(0, 243, 255, 0.4) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:disabled {
    border-color: var(--border2) !important;
    color: var(--muted) !important;
    opacity: 0.5 !important;
    cursor: not-allowed !important;
    box-shadow: none !important;
}

/* Reset button styling */
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: transparent !important;
    border-color: var(--border2) !important;
    color: var(--muted) !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover:not(:disabled) {
    border-color: var(--danger) !important;
    color: var(--danger) !important;
    background: rgba(255, 42, 109, 0.1) !important;
    box-shadow: 0 0 20px rgba(255, 42, 109, 0.25) !important;
}

/* ── Progress Bar ── */
[data-testid="stProgressBar"] > div {
    background: rgba(14, 19, 34, 0.8) !important;
    border-radius: 4px !important;
    height: 6px !important;
    border: 1px solid var(--border) !important;
}
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--success)) !important;
    border-radius: 4px !important;
    box-shadow: 0 0 12px var(--accent) !important;
}

/* ── Pipeline Steps Tracker Grid ── */
.pipeline-card {
    background: rgba(10, 14, 26, 0.85);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem 1.8rem;
    margin: 1.5rem 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}
.pipeline-header {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 3px;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.steps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 10px;
}
.step-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 8px;
    text-align: center;
    transition: all 0.3s ease;
}
.step-item.done {
    border-color: rgba(0, 255, 157, 0.4);
    background: rgba(0, 255, 157, 0.05);
    box-shadow: 0 0 12px rgba(0, 255, 157, 0.08);
}
.step-item.running {
    border-color: rgba(0, 243, 255, 0.6);
    background: rgba(0, 243, 255, 0.08);
    box-shadow: 0 0 18px rgba(0, 243, 255, 0.2);
    animation: pulse-border 1.4s infinite alternate;
}
.step-item.pending { opacity: 0.4; }

@keyframes pulse-border {
    0% { box-shadow: 0 0 8px rgba(0, 243, 255, 0.1); border-color: rgba(0, 243, 255, 0.4); }
    100% { box-shadow: 0 0 20px rgba(0, 243, 255, 0.4); border-color: var(--accent); }
}

.step-icon  { font-size: 20px; margin-bottom: 4px; }
.step-name  {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 1.5px;
    color: var(--text);
    text-transform: uppercase;
    margin-bottom: 4px;
    font-weight: 600;
}
.step-state {
    font-size: 9px;
    font-family: var(--mono);
}
.step-state.s-done    { color: var(--success); font-weight: 600; }
.step-state.s-running { color: var(--accent); font-weight: 600; }
.step-state.s-pending { color: var(--muted); }

/* ── Status Line ── */
.status-line {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--accent);
    letter-spacing: 1px;
    padding: 8px 0;
}

/* ── Results Overview Metrics ── */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 2rem;
}
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; bottom: 0;
    width: 3px;
    background: var(--accent);
}
.metric-label {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 2px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 4px;
}
.metric-value {
    font-family: var(--font-heading);
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
}

/* ── Hash Display Block ── */
.hash-block {
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 8px;
    padding: 14px 20px;
    margin-bottom: 1.8rem;
    display: flex;
    align-items: center;
    gap: 16px;
    font-family: var(--mono);
}
.hash-lbl {
    font-size: 11px;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    white-space: nowrap;
    border-right: 1px solid var(--border2);
    padding-right: 16px;
}
.hash-val {
    font-size: 12px;
    color: var(--accent);
    word-break: break-all;
}

/* ── Tabs Override ── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--card) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 8px !important;
    padding: 6px !important;
    gap: 6px !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: var(--font-heading) !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    border-radius: 6px !important;
    padding: 10px 24px !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: rgba(0, 243, 255, 0.1) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(0, 243, 255, 0.3) !important;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.15) !important;
}

/* ── Report Toolbar ── */
.report-bar {
    background: var(--card);
    border: 1px solid var(--border2);
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.report-bar-left {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 1.5px;
}
.report-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--success);
    box-shadow: 0 0 8px var(--success);
    animation: blink 2s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
.report-frame-wrap {
    border: 1px solid var(--border2);
    border-top: none;
    border-radius: 0 0 8px 8px;
    overflow: hidden;
}

/* ── Download Button ── */
[data-testid="stDownloadButton"] > button {
    background: rgba(0, 255, 157, 0.08) !important;
    border: 1px solid rgba(0, 255, 157, 0.35) !important;
    color: var(--success) !important;
    font-family: var(--font-heading) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: var(--success) !important;
    color: #000 !important;
    box-shadow: 0 0 20px var(--success) !important;
}

.open-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    background: rgba(0, 243, 255, 0.08);
    border: 1px solid rgba(0, 243, 255, 0.35);
    color: var(--accent) !important;
    font-family: var(--font-heading);
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    text-decoration: none !important;
    border-radius: 6px;
    padding: 0.6rem 1.5rem;
    transition: all 0.2s ease;
    width: 100%;
}
.open-link:hover {
    background: var(--accent);
    color: #000 !important;
    box-shadow: 0 0 20px var(--accent);
}
</style>
""", unsafe_allow_html=True)

# ── Session State Defaults ──
defaults = {
    "done": False,
    "batch_results": [],
    "error": None,
    "running": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Pipeline Steps Definition ──
STEPS = [
    ("hash",    "🔑", "Hash"),
    ("upx",     "📦", "UPX"),
    ("floss",   "🔍", "Floss"),
    ("vt",      "🌐", "VT"),
    ("static",  "📄", "Static"),
    ("dynamic", "⚡", "Dynamic"),
    ("yara",    "🎯", "Yara"),
    ("agg",     "🧩", "Agg"),
    ("insight", "🧠", "Insight"),
    ("summary", "📊", "Report"),
]

# ── HERO HEADER ──
st.markdown("""
<div class="hero-wrap" style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; width: 100%;">
    <div class="hero-tag">Automated Threat Intelligence & Malware Analysis Platform</div>
    <div class="hero-title">ThreatLens</div>
    <div style="display: flex; justify-content: center; width: 100%;">
        <p class="hero-sub" style="text-align: center; text-align-last: center; margin: 0 auto 2rem; max-width: 650px; width: 100%;">
            Drop binary samples or specify target directories to perform automated static PE analysis,
            YARA rule scanning, FLOSS string extraction, VirusTotal threat lookup, and AI report synthesis.
        </p>
    </div>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ── SCAN TARGET SELECTION ──
st.markdown('<div class="card-label">Scan Target Selection</div>', unsafe_allow_html=True)

scan_mode = st.radio(
    "Scan Mode",
    ["Upload Files (Single or Multiple)", "Directory Scan"],
    horizontal=True,
    label_visibility="collapsed"
)

uploaded_files = None
dir_path = ""

if scan_mode == "Upload Files (Single or Multiple)":
    uploaded_files = st.file_uploader(
        "Drop malware binaries here",
        type=None,
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
else:
    dir_path = st.text_input(
        "Directory Path",
        placeholder="Enter absolute directory path e.g. C:\\MalwareSamples",
        label_visibility="collapsed"
    )

has_targets = (uploaded_files is not None and len(uploaded_files) > 0) if scan_mode == "Upload Files (Single or Multiple)" else (bool(dir_path and os.path.isdir(dir_path)))

c1, c2, _ = st.columns([3, 1.2, 5])
with c1:
    run_btn = st.button(
        "⬡  RUN ANALYSIS",
        use_container_width=True,
        disabled=(not has_targets or st.session_state.running),
    )
with c2:
    reset_btn = st.button("↺  RESET", use_container_width=True)

# ── RESET ACTION ──
if reset_btn:
    for k, v in defaults.items():
        st.session_state[k] = v
    st.rerun()

# ── RUN PIPELINE ACTION ──
if run_btn and has_targets and not st.session_state.done:
    st.session_state.running = True
    st.session_state.batch_results = []
    st.session_state.error = None

    targets = []
    if scan_mode == "Upload Files (Single or Multiple)":
        for u in uploaded_files:
            suffix = Path(u.name).suffix or ".bin"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(u.read())
                targets.append((u.name, tmp.name, True))
    else:
        for root, _, files in os.walk(dir_path):
            for f in files:
                full_p = os.path.join(root, f)
                targets.append((f, full_p, False))

    if not targets:
        st.warning("No target files found for analysis.")
        st.session_state.running = False
    else:
        pipeline_card_ph = st.empty()
        progress_ph = st.empty()
        status_ph   = st.empty()

        def render_steps_ui(completed: set, running_key: str | None, current_file: str, batch_idx: int, total_files: int):
            cards_html = ""
            for key, icon, label in STEPS:
                if key in completed:
                    cls, sc, st_txt = "done", "s-done", "✓ DONE"
                elif key == running_key:
                    cls, sc, st_txt = "running", "s-running", "⟳ RUNNING"
                else:
                    cls, sc, st_txt = "pending", "s-pending", "· QUEUED"
                cards_html += f"""
                <div class="step-item {cls}">
                    <div class="step-icon">{icon}</div>
                    <div class="step-name">{label}</div>
                    <div class="step-state {sc}">{st_txt}</div>
                </div>"""

            pipeline_card_ph.markdown(
                f"""
                <div class="pipeline-card">
                    <div class="pipeline-header">
                        <span>◈ BATCH PIPELINE EXECUTION</span>
                        <span>SAMPLE [{batch_idx}/{total_files}]: <b>{current_file}</b></span>
                    </div>
                    <div class="steps-grid">{cards_html}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        import builtins, queue, threading, time

        for idx, (filename, file_path, is_temp) in enumerate(targets, 1):
            render_steps_ui(set(), "hash", filename, idx, len(targets))
            progress_ph.progress(0.0)

            print_q = queue.Queue()
            _orig_print = builtins.print

            def _patched_print(*args, **kwargs):
                _orig_print(*args, **kwargs)
                print_q.put(" ".join(str(a) for a in args))

            builtins.print = _patched_print
            result_q = queue.Queue()

            def _run(path):
                try:
                    from graph import graph
                    out = graph.invoke({"file_path": path})
                    result_q.put(("ok", out))
                except Exception as e:
                    result_q.put(("err", str(e)))

            t = threading.Thread(target=_run, args=(file_path,), daemon=True)
            t.start()

            step_order = [s[0] for s in STEPS]
            completed  = set()

            while t.is_alive() or not print_q.empty():
                try:
                    msg = print_q.get_nowait()
                    matched = next(
                        (k for k in step_order if msg.strip().lower().startswith(k)),
                        None,
                    )
                    if matched:
                        completed.add(matched)
                        s_idx = step_order.index(matched)
                        nxt   = step_order[s_idx + 1] if s_idx + 1 < len(step_order) else None
                        pct   = len(completed) / len(STEPS)
                        render_steps_ui(completed, nxt, filename, idx, len(targets))
                        progress_ph.progress(min(pct, 1.0))
                        status_ph.markdown(
                            f'<div class="status-line">▶ [{idx}/{len(targets)}] {filename} — {matched.upper()} complete '
                            f'({int(pct*100)}%)</div>',
                            unsafe_allow_html=True,
                        )
                except queue.Empty:
                    time.sleep(0.1)

            builtins.print = _orig_print
            render_steps_ui(completed, None, filename, idx, len(targets))
            progress_ph.progress(1.0)

            if is_temp and os.path.exists(file_path):
                try: os.unlink(file_path)
                except: pass

            status, payload = result_q.get()

            def _read(path):
                return open(path, encoding="utf-8").read() if os.path.exists(path) else None

            if status == "err":
                st.session_state.batch_results.append({
                    "filename": filename,
                    "file_hash": "N/A",
                    "summary_html": None,
                    "full_html": None,
                    "vt_detection": "Error",
                    "upx_packed": "N/A",
                    "yara_severity": "N/A",
                    "threat_label": "N/A",
                    "error": payload
                })
            else:
                dyn = payload.get("dynamic_analysis") or {}
                upx_res = payload.get("upx_result") or {}
                yara_res = payload.get("yara_result") or {}

                st.session_state.batch_results.append({
                    "filename": filename,
                    "file_hash": payload.get("file_hash", "N/A"),
                    "summary_html": payload.get("summary_html") or _read("outputs/summary_report.html"),
                    "full_html": payload.get("full_report_html") or _read("outputs/full_report.html"),
                    "vt_detection": dyn.get("detection_ratio", "N/A"),
                    "upx_packed": "Yes" if upx_res.get("packed") else "No",
                    "yara_severity": yara_res.get("severity", "none").upper(),
                    "threat_label": dyn.get("threat_label", "unknown"),
                    "error": None
                })

        st.session_state.done = True
        st.session_state.running = False
        st.rerun()

# ── ERROR DISPLAY ──
if st.session_state.error:
    st.error(f"Pipeline error: {st.session_state.error}")

# ── RESULTS DISPLAY ──
if st.session_state.done and st.session_state.batch_results:
    st.markdown('<div class="hero-line"></div>', unsafe_allow_html=True)

    results = st.session_state.batch_results

    # Batch summary overview table if > 1 file
    if len(results) > 1:
        st.markdown("### 📊 Batch Analysis Overview")
        table_data = []
        for r in results:
            table_data.append({
                "File Name": r["filename"],
                "SHA-256": r["file_hash"],
                "Threat Label": r["threat_label"],
                "YARA Severity": r["yara_severity"],
                "UPX Packed": r["upx_packed"],
                "VT Detection": r["vt_detection"],
                "Status": "Error" if r["error"] else "Analyzed"
            })
        st.dataframe(table_data, use_container_width=True)
        st.markdown('<div class="hero-line"></div>', unsafe_allow_html=True)

    filenames = [f"{r['filename']} ({r['file_hash'][:12]}...)" for r in results]
    selected_idx = st.selectbox(
        "Select Sample to Inspect Detailed Threat Intelligence",
        options=list(range(len(filenames))),
        format_func=lambda i: filenames[i],
        index=0
    )
    selected_res = results[selected_idx]

    if selected_res["error"]:
        st.error(f"Failed to analyze {selected_res['filename']}: {selected_res['error']}")
    else:
        # Overview Metric Cards
        st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-card" style="border-left-color: var(--accent);">
                <div class="metric-label">VirusTotal Score</div>
                <div class="metric-value" style="color: var(--accent);">{selected_res['vt_detection']}</div>
            </div>
            <div class="metric-card" style="border-left-color: var(--danger);">
                <div class="metric-label">YARA Severity</div>
                <div class="metric-value" style="color: var(--danger);">{selected_res['yara_severity']}</div>
            </div>
            <div class="metric-card" style="border-left-color: var(--warning);">
                <div class="metric-label">UPX Packer Status</div>
                <div class="metric-value" style="color: var(--warning);">{selected_res['upx_packed']}</div>
            </div>
            <div class="metric-card" style="border-left-color: var(--accent2);">
                <div class="metric-label">Suggested Threat Label</div>
                <div class="metric-value" style="color: var(--accent2);">{selected_res['threat_label']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Hash bar
        st.markdown(
            f'<div class="hash-block">'
            f'<span class="hash-lbl">SHA-256</span>'
            f'<span class="hash-val">{selected_res["file_hash"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Tabs
        tab_sum, tab_full = st.tabs([
            "  📊  SUMMARY REPORT  ",
            "  📄  FULL TECHNICAL REPORT  ",
        ])

        def _render_tab(html: str | None, label: str, fname: str):
            if not html:
                st.warning(f"{label} not available.")
                return

            b64 = base64.b64encode(html.encode("utf-8")).decode()

            ca, cb, _ = st.columns([2.2, 2.2, 5.6])
            with ca:
                st.download_button(
                    label="⬇  DOWNLOAD REPORT",
                    data=html.encode("utf-8"),
                    file_name=fname,
                    mime="text/html",
                    use_container_width=True,
                    key=f"dl_{fname}_{selected_idx}"
                )
            with cb:
                st.components.v1.html(
                    f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
                        <style>
                            body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; }}
                            .open-btn {{
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                background: rgba(0, 243, 255, 0.08);
                                border: 1px solid rgba(0, 243, 255, 0.35);
                                color: #00f3ff;
                                font-family: 'Rajdhani', sans-serif;
                                font-size: 14px;
                                font-weight: 600;
                                letter-spacing: 1.5px;
                                text-transform: uppercase;
                                border-radius: 6px;
                                padding: 0.6rem 1.5rem;
                                transition: all 0.2s ease;
                                width: 100%;
                                box-sizing: border-box;
                                cursor: pointer;
                                text-decoration: none;
                            }}
                            .open-btn:hover {{
                                background: #00f3ff;
                                color: #000;
                                box-shadow: 0 0 20px #00f3ff;
                            }}
                        </style>
                    </head>
                    <body>
                        <button class="open-btn" onclick="openFullscreen()">↗&nbsp; OPEN FULLSCREEN</button>
                        <script>
                            function openFullscreen() {{
                                // Decode base64 to Unicode string securely
                                const b64 = "{b64}";
                                const binStr = atob(b64);
                                const bytes = new Uint8Array(binStr.length);
                                for (let i = 0; i < binStr.length; i++) {{
                                    bytes[i] = binStr.charCodeAt(i);
                                }}
                                const blob = new Blob([bytes], {{type: 'text/html;charset=utf-8'}});
                                const url = URL.createObjectURL(blob);
                                window.open(url, '_blank');
                            }}
                        </script>
                    </body>
                    </html>
                    """,
                    height=45
                )
            st.markdown(
                '<div class="report-bar">'
                '  <div class="report-bar-left"><div class="report-dot"></div>LIVE REPORT PREVIEW</div>'
                '  <span style="font-family:\'Share Tech Mono\',monospace;font-size:10px;'
                '  color:var(--muted);letter-spacing:2px;">THREATLENS INTERACTIVE REPORT</span>'
                '</div>'
                '<div class="report-frame-wrap">',
                unsafe_allow_html=True,
            )
            st.components.v1.html(html, height=850, scrolling=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_sum:
            _render_tab(
                selected_res["summary_html"],
                "Summary Report",
                f"{selected_res['filename']}_summary.html",
            )

        with tab_full:
            _render_tab(
                selected_res["full_html"],
                "Full Technical Report",
                f"{selected_res['filename']}_full_report.html",
            )

# ── FOOTER ──
st.markdown("""
<div style="
    text-align: center;
    margin-top: 5rem;
    padding: 2.5rem 0 1.5rem;
    border-top: 1px solid var(--border);
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
">
    ThreatLens · LangGraph Multi-Agent Architecture · Powered by Groq AI
</div>
""", unsafe_allow_html=True)
