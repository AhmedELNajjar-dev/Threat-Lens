import os
import markdown
from datetime import datetime
from state import GraphState


def render_report_html_node(state: GraphState):
    data = state["aggregated"]

    def md_to_html(text: str) -> str:
        if not text:
            return "<p>No data available</p>"
        return markdown.markdown(text, extensions=["tables", "fenced_code"])

    file_hash = data.get("file_hash", "N/A")
    now       = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sections = [
        ("UPX Analysis",     "upx",     "🔒"),
        ("FLOSS Strings",    "floss",   "🔍"),
        ("Static Analysis",  "static",  "📄"),
        ("Dynamic Analysis", "dynamic", "⚡"),
        ("YARA Matches",     "yara",    "🎯"),
    ]

    sidebar_links = "\n".join(
        f'<a href="#{key}" class="nav-link">{icon} {title}</a>'
        for title, key, icon in sections
    )

    section_cards = ""
    for i, (title, key, icon) in enumerate(sections, 1):
        content_html = md_to_html(data.get(key, ""))
        section_cards += f"""
        <section id="{key}" class="card">
            <div class="card-header" onclick="toggleSection('{key}')">
                <div class="card-title">
                    <span class="section-badge">{i}</span>
                    <span>{icon} {title}</span>
                </div>
                <span class="toggle-arrow" id="arrow-{key}">▼</span>
            </div>
            <div class="card-body" id="body-{key}">
                <div class="md-content">{content_html}</div>
            </div>
        </section>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Malware Analysis Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg:        #0a0a0f;
            --card:      #12121a;
            --border:    #1e1e2e;
            --accent:    #6366f1;
            --danger:    #ef4444;
            --warning:   #f97316;
            --caution:   #eab308;
            --success:   #22c55e;
            --text:      #e2e8f0;
            --muted:     #94a3b8;
            --mono:      #a78bfa;
            --sidebar-w: 240px;
            --header-h:  60px;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            background: var(--bg);
            color: var(--text);
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            line-height: 1.7;
        }}

        .header {{
            position: fixed;
            top: 0; left: 0; right: 0;
            height: var(--header-h);
            background: rgba(10,10,15,0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            padding: 0 24px;
            gap: 16px;
            z-index: 100;
        }}
        .header-title {{
            font-weight: 700;
            font-size: 15px;
            color: var(--accent);
            white-space: nowrap;
        }}
        .header-hash {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: var(--muted);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .header-accent-line {{
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--accent), transparent);
        }}

        .sidebar {{
            position: fixed;
            top: var(--header-h);
            left: 0;
            width: var(--sidebar-w);
            height: calc(100vh - var(--header-h));
            background: #0d0d14;
            border-right: 1px solid var(--border);
            padding: 24px 12px;
            overflow-y: auto;
        }}
        .sidebar-label {{
            font-size: 10px;
            font-weight: 600;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 0 12px;
            margin-bottom: 12px;
        }}
        .nav-link {{
            display: block;
            padding: 9px 14px;
            border-radius: 8px;
            color: var(--muted);
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.2s;
            margin-bottom: 4px;
        }}
        .nav-link:hover {{ background: var(--border); color: var(--text); }}
        .nav-link.active {{
            background: rgba(99,102,241,0.15);
            color: var(--accent);
            border-left: 3px solid var(--accent);
        }}

        .main {{
            margin-left: var(--sidebar-w);
            margin-top: var(--header-h);
            padding: 32px 40px;
            max-width: 960px;
        }}

        .hash-banner {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .hash-label {{
            font-size: 11px;
            color: var(--muted);
            font-weight: 600;
            text-transform: uppercase;
            white-space: nowrap;
        }}
        .hash-value {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: var(--mono);
            word-break: break-all;
        }}

        .card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            margin-bottom: 16px;
            overflow: hidden;
            scroll-margin-top: calc(var(--header-h) + 16px);
        }}
        .card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px;
            cursor: pointer;
            user-select: none;
            border-bottom: 1px solid var(--border);
            transition: background 0.2s;
        }}
        .card-header:hover {{ background: rgba(255,255,255,0.03); }}
        .card-title {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 600;
            font-size: 14px;
        }}
        .section-badge {{
            width: 26px; height: 26px;
            background: rgba(99,102,241,0.2);
            color: var(--accent);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
        }}
        .toggle-arrow {{
            color: var(--muted);
            font-size: 12px;
            transition: transform 0.3s;
        }}
        .toggle-arrow.collapsed {{ transform: rotate(-90deg); }}

        .card-body {{
            padding: 20px;
            overflow: hidden;
            max-height: 10000px;
            transition: max-height 0.4s ease, padding 0.3s ease;
        }}
        .card-body.collapsed {{
            max-height: 0;
            padding-top: 0;
            padding-bottom: 0;
        }}

        .md-content h1, .md-content h2 {{
            font-size: 14px;
            font-weight: 700;
            color: var(--accent);
            margin: 20px 0 10px;
            padding-bottom: 6px;
            border-bottom: 1px solid var(--border);
        }}
        .md-content h3 {{
            font-size: 13px;
            font-weight: 600;
            color: var(--text);
            margin: 14px 0 8px;
        }}
        .md-content ul {{ padding-left: 20px; margin: 8px 0; }}
        .md-content li {{ margin: 4px 0; color: var(--muted); }}
        .md-content li strong {{ color: var(--text); }}
        .md-content code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: var(--mono);
            background: rgba(167,139,250,0.1);
            padding: 2px 6px;
            border-radius: 4px;
        }}
        .md-content p {{ margin: 8px 0; color: var(--muted); }}
        .md-content strong {{ color: var(--text); }}

        .footer {{
            margin-left: var(--sidebar-w);
            text-align: center;
            padding: 32px;
            color: var(--muted);
            font-size: 12px;
            border-top: 1px solid var(--border);
        }}
    </style>
</head>
<body>

    <header class="header">
        <span class="header-title">🛡 Malware Analysis Report</span>
        <span class="header-hash">{file_hash}</span>
        <div class="header-accent-line"></div>
    </header>

    <nav class="sidebar">
        <div class="sidebar-label">Sections</div>
        {sidebar_links}
    </nav>

    <main class="main">
        <div class="hash-banner">
            <span class="hash-label">SHA256</span>
            <span class="hash-value">{file_hash}</span>
        </div>
        {section_cards}
    </main>

    <footer class="footer">
        Generated on {now} &nbsp;|&nbsp; Malware Analysis Pipeline
    </footer>

    <script>
        function toggleSection(key) {{
            const body  = document.getElementById('body-'  + key);
            const arrow = document.getElementById('arrow-' + key);
            body.classList.toggle('collapsed');
            arrow.classList.toggle('collapsed');
        }}

        const sections = document.querySelectorAll('section.card');
        const navLinks = document.querySelectorAll('.nav-link');

        const observer = new IntersectionObserver(entries => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    navLinks.forEach(l => l.classList.remove('active'));
                    const active = document.querySelector(`.nav-link[href="#${{entry.target.id}}"]`);
                    if (active) active.classList.add('active');
                }}
            }});
        }}, {{ rootMargin: '-40% 0px -55% 0px' }});

        sections.forEach(s => observer.observe(s));

        navLinks.forEach(link => {{
            link.addEventListener('click', e => {{
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) target.scrollIntoView({{ behavior: 'smooth' }});
            }});
        }});
    </script>
</body>
</html>"""

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/full_report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("full_report_html")
    return {"full_report_html": html}
