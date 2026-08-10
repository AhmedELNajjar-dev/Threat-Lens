import os
from state import GraphState
from utils.llm import call_llm


def summary_report_node(state: GraphState):
    insights = state["insights"]

    prompt = f"""You are an elite frontend developer and malware analyst.

You will receive a threat intelligence report in markdown format.
Your task is to convert it into a premium interactive single-file HTML dashboard.

STRICT RULES:
- Do NOT change, summarize, interpret, or generate any new information
- Preserve ALL report content exactly as provided
- Only transform the report into an HTML interface
- Return ONLY raw HTML
- No markdown
- No explanations
- No code blocks

TECH STACK:
- Use Bootstrap 5 via CDN
- Use Bootstrap Icons via CDN
- Use Google Fonts:
  - Inter
  - JetBrains Mono
- Use vanilla JavaScript only
- Everything must exist in ONE HTML file

DESIGN GOAL:
Create a visually impressive modern cybersecurity dashboard similar to:
- Linear
- Vercel
- Stripe Dashboard
- Premium SOC/threat intelligence platforms

The UI must feel:
- Interactive
- Cinematic
- High-tech
- Clean
- Modern
- Premium
- Animated
- Responsive

AVOID:
- Flat gray Bootstrap cards
- Generic admin dashboard appearance
- Plain white text on black background
- Basic Bootstrap-only styling
- Huge empty spaces
- Boring layouts

LAYOUT:
- Sticky top navbar
- Responsive collapsible mobile menu
- Vertical stacked sections
- Smooth scrolling navigation
- Large centered container
- Beautiful spacing and layout hierarchy
- Use generous spacing between content blocks

NAVBAR:
Create a premium sticky navbar with:
- Frosted glass effect
- Blur background
- Logo/title on left
- Navigation links on right
- Smooth hover underline animation
- Active section highlighting while scrolling
- Small glowing accent border at bottom
- Compact premium appearance
- Subtle shadow underneath

Navbar sections:
- Summary
- Classification
- Behavior
- IOCs
- Findings
- Risk
- Recommendations

BACKGROUND:
- Use layered dark gradients
- Add subtle radial glow effects
- Add blur overlays and visual depth
- Use elegant cyber-style lighting effects
- Background must feel alive and premium
- Add subtle floating glow particles or blurred shapes if appropriate

COLOR SYSTEM:
- Use harmonious dark cyber colors
- Indigo/cyan/purple accents
- Elegant gradients
- Soft glow effects
- Subtle transparency
- Avoid overly bright or harsh colors

TYPOGRAPHY:
- Inter font for UI
- JetBrains Mono for hashes/code/IOCs
- Strong heading hierarchy
- Elegant spacing
- Softer secondary text
- Styled code pills for hashes and technical values
- Better paragraph spacing and readability
- Proper line-height throughout the page

HEADER AREA:
- Show report title beautifully
- Display hash/file information in styled pills
- Add severity badge if available
- Add animated gradient divider
- Use modern spacing and alignment

SECTION BLOCKS:
- Every major section MUST appear inside its own premium card block
- Each block should visually stand apart from the background
- Use:
  * layered glassmorphism surfaces
  * soft gradients
  * subtle border glow
  * shadow depth
  * rounded corners (18px–24px)
  * internal padding
  * spacing between blocks

- Do NOT render sections directly on the page background
- Every section must feel contained inside a modern component/card

SECTION CONTAINER STYLE:
- Use a darker outer background with a slightly lighter inner card
- Add subtle gradient border effects
- Add hover lift animation:
  transform: translateY(-4px)
- Add smooth transition effects
- Add soft blue/purple glow on hover

SECTION DESIGN:
- Each section must:
  * be collapsible
  * have smooth animations
  * use layered surfaces
  * have premium depth
  * contain elegant spacing
  * include animated chevron rotation
  * use Bootstrap Icons beside titles

- Add animated accent line under section titles
- Add section spacing and visual hierarchy
- Add smooth reveal animations on scroll

INTERACTIVITY:
- Smooth section collapse/expand
- Animated arrow rotation
- Scroll reveal animations
- Hover animations
- Copy-to-clipboard buttons
- Toast/check animation after copying
- Active navbar section tracking
- Smooth scrolling navigation
- Tooltip animations on buttons

TABLES:
- Modern IOC tables
- Bootstrap responsive tables
- Rounded containers
- Alternating row backgrounds
- Hover row highlight
- Sticky headers if possible
- Styled action buttons
- Modern badge styling for important values

LISTS & CONTENT:
- Lists should feel modern and properly spaced
- Technical indicators should appear inside styled pills/tags
- Important values should visually stand out
- Use grouped content containers where appropriate

VISUAL EFFECTS:
- Glow hover effects
- Subtle animated gradients
- Card hover elevation
- Fade-in animations
- Smooth transitions everywhere
- Modern polished SaaS appearance
- Add subtle lighting depth to cards and sections

FOOTER:
- Minimal elegant footer
- Generated timestamp
- Muted text styling

IMPORTANT:
- The final result must feel like a real premium cybersecurity SaaS product
- Make the UI highly interactive and visually rich
- Focus heavily on polish, animation, depth, and modern UX
- Do NOT create plain Bootstrap cards
- Bootstrap should be enhanced with strong custom CSS
- Avoid rendering plain text directly on the page background
- Every major content area should feel isolated and visually polished
- The design should look handcrafted and premium

Report content to convert:
{insights}
"""

    html = call_llm(prompt)

    if html.startswith("```"):
        html = html.split("```")[1]
        if html.startswith("html"):
            html = html[4:]
        html = html.rsplit("```", 1)[0]

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/summary_report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("summary")
    return {"summary_html": html}
