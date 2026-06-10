"""
Generate SwarmDesk Project Deck PDF (10 slides)
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

W, H = A4  # 595 x 842 pt

# ── Colours ──────────────────────────────────────────────────────────
BG      = colors.HexColor("#080c14")
SURFACE = colors.HexColor("#0d1424")
CARD    = colors.HexColor("#111927")
INDIGO  = colors.HexColor("#6366f1")
CYAN    = colors.HexColor("#06b6d4")
EMERALD = colors.HexColor("#10b981")
AMBER   = colors.HexColor("#f59e0b")
WHITE   = colors.HexColor("#f1f5f9")
MUTED   = colors.HexColor("#94a3b8")
DIM     = colors.HexColor("#475569")

def draw_bg(c, gradient_color=None):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Subtle grid
    c.setStrokeColor(colors.HexColor("#1a2236"))
    c.setLineWidth(0.3)
    step = 40
    for x in range(0, int(W)+step, step):
        c.line(x, 0, x, H)
    for y in range(0, int(H)+step, step):
        c.line(0, y, W, y)
    # Orb
    if gradient_color:
        c.setFillColor(gradient_color)
        c.setFillAlpha(0.08)
        c.circle(W*0.85, H*0.85, 200, fill=1, stroke=0)
        c.setFillAlpha(1.0)

def draw_card(c, x, y, w, h, border_color=None):
    c.setFillColor(CARD)
    c.setStrokeColor(border_color or colors.HexColor("#1e2d45"))
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)

def slide_label(c, text, color=INDIGO):
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(color)
    c.drawString(40, H - 38, text.upper())

def slide_title(c, text, y=H-65, size=28, color=WHITE):
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(color)
    c.drawString(40, y, text)

def slide_subtitle(c, text, y=H-85, color=MUTED):
    c.setFont("Helvetica", 11)
    c.setFillColor(color)
    c.drawString(40, y, text)

def footer(c, page_num, total=10):
    c.setFont("Helvetica", 7)
    c.setFillColor(DIM)
    c.drawString(40, 20, "SwarmDesk · Microsoft AI Hackathon 2026 · Theme 05: Agent Swarms")
    c.drawRightString(W - 40, 20, f"{page_num} / {total}")
    c.setStrokeColor(colors.HexColor("#1e2d45"))
    c.setLineWidth(0.5)
    c.line(40, 32, W-40, 32)

def accent_bar(c, color=INDIGO):
    c.setFillColor(color)
    c.rect(0, H-5, W, 5, fill=1, stroke=0)

def hex_bullet(c, x, y, size=8):
    c.setFillColor(INDIGO)
    c.setFont("Helvetica", size)
    c.drawString(x, y, "⬡")

# ─────────────────────────────────────────────────────────────────────

def slide1_cover(c):
    draw_bg(c, INDIGO)
    accent_bar(c)
    # Huge hex watermark
    c.setFont("Helvetica-Bold", 200)
    c.setFillColor(INDIGO)
    c.setFillAlpha(0.06)
    c.drawString(-20, H//2 - 100, "⬡")
    c.setFillAlpha(1.0)
    # Eyebrow
    c.setFillColor(SURFACE)
    c.roundRect(40, H-75, 220, 22, 5, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(INDIGO)
    c.drawString(48, H-65, "⬡  THEME 05 · AGENT SWARMS")
    # Title
    c.setFont("Helvetica-Bold", 48)
    c.setFillColor(WHITE)
    c.drawString(40, H-140, "SwarmDesk")
    # Gradient line under title
    c.setFillColor(INDIGO)
    c.rect(40, H-148, 320, 3, fill=1, stroke=0)
    # Subtitle
    c.setFont("Helvetica", 16)
    c.setFillColor(CYAN)
    c.drawString(40, H-172, "Multi-Agent AI Productivity System")
    # Description
    c.setFont("Helvetica", 11)
    c.setFillColor(MUTED)
    lines = [
        "Orchestrate a swarm of 4 specialized AI agents —",
        "Planner · Researcher · Writer · Validator —",
        "to tackle complex professional tasks collaboratively."
    ]
    for i, line in enumerate(lines):
        c.drawString(40, H-200 - i*18, line)
    # Agent pills
    agents = [("🗺️ Planner", INDIGO), ("🔍 Researcher", CYAN), ("✍️ Writer", EMERALD), ("✅ Validator", AMBER)]
    cx = 40
    for label, clr in agents:
        w_pill = 100
        c.setFillColor(clr)
        c.setFillAlpha(0.12)
        c.roundRect(cx, H-310, w_pill, 22, 5, fill=1, stroke=0)
        c.setFillAlpha(1.0)
        c.setStrokeColor(clr)
        c.setLineWidth(1)
        c.roundRect(cx, H-310, w_pill, 22, 5, fill=0, stroke=1)
        c.setFont("Helvetica", 9)
        c.setFillColor(clr)
        c.drawString(cx+8, H-302, label)
        cx += w_pill + 10
    # Hackathon info box
    draw_card(c, 40, 80, W-80, 60)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(WHITE)
    c.drawString(56, 124, "Microsoft AI Hackathon 2026")
    c.setFont("Helvetica", 9)
    c.setFillColor(MUTED)
    c.drawString(56, 108, "3 May – 30 June 2026  ·  Python · FastAPI · Azure OpenAI · SSE Streaming")
    footer(c, 1)
    c.showPage()

def slide2_problem(c):
    draw_bg(c, CYAN)
    accent_bar(c, CYAN)
    slide_label(c, "01 — Problem Statement", CYAN)
    slide_title(c, "The productivity gap is real", y=H-65, size=26)
    slide_subtitle(c, "Knowledge workers waste hours on tasks that demand synthesis, research, and judgment.", y=H-90)
    # Problem cards
    problems = [
        ("⏱️", "Context Switching", "Professionals switch between research, planning, writing, and reviewing — losing flow and quality each time."),
        ("🧠", "Cognitive Overload", "Complex tasks require holding too much context in mind simultaneously, leading to shallow outputs."),
        ("🔄", "Iteration Hell", "First drafts require multiple manual revision cycles — each one costing more time and energy."),
        ("🚫", "Single-AI Bottleneck", "Asking one AI to plan, research, write, and validate in a single prompt produces generic, mediocre results."),
    ]
    gy = H - 115
    card_h = 100
    card_w = (W - 80 - 15) / 2
    for i, (icon, title, desc) in enumerate(problems):
        col = i % 2
        row = i // 2
        cx = 40 + col * (card_w + 15)
        cy = gy - row * (card_h + 12)
        draw_card(c, cx, cy - card_h, card_w, card_h)
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(WHITE)
        c.drawString(cx+14, cy-28, icon)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(CYAN)
        c.drawString(cx+14, cy-46, title)
        # Wrap description
        c.setFont("Helvetica", 8.5)
        c.setFillColor(MUTED)
        words = desc.split()
        line = ""; dy = cy - 60
        for word in words:
            test = line + word + " "
            if c.stringWidth(test, "Helvetica", 8.5) > card_w - 28:
                c.drawString(cx+14, dy, line.strip()); line = word + " "; dy -= 13
            else:
                line = test
        if line: c.drawString(cx+14, dy, line.strip())
    footer(c, 2)
    c.showPage()

def slide3_solution(c):
    draw_bg(c, EMERALD)
    accent_bar(c, EMERALD)
    slide_label(c, "02 — Solution Overview", EMERALD)
    slide_title(c, "SwarmDesk: Agents that collaborate", y=H-65, size=26)
    slide_subtitle(c, "Four specialized agents work sequentially, each building on the last — like a high-performance team.", y=H-90)
    # Pipeline boxes
    agents = [
        ("🗺️", "PLANNER", "Breaks task into actionable steps", INDIGO),
        ("🔍", "RESEARCHER", "Gathers knowledge & frameworks", CYAN),
        ("✍️", "WRITER", "Produces the polished deliverable", EMERALD),
        ("✅", "VALIDATOR", "Reviews, scores & improves output", AMBER),
    ]
    bw = (W - 80 - 30) / 4
    by = H - 130
    for i, (icon, name, desc, clr) in enumerate(agents):
        bx = 40 + i * (bw + 10)
        # Card
        c.setFillColor(CARD)
        c.setStrokeColor(clr)
        c.setLineWidth(1.5)
        c.roundRect(bx, by - 110, bw, 110, 6, fill=1, stroke=1)
        # Icon
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(clr)
        c.drawCentredString(bx + bw/2, by - 32, icon)
        # Name
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(clr)
        c.drawCentredString(bx + bw/2, by - 52, name)
        # Desc
        c.setFont("Helvetica", 7.5)
        c.setFillColor(MUTED)
        words = desc.split()
        line = ""; dy = by - 68
        for word in words:
            test = line + word + " "
            if c.stringWidth(test, "Helvetica", 7.5) > bw - 16:
                c.drawCentredString(bx + bw/2, dy, line.strip()); line = word + " "; dy -= 11
            else:
                line = test
        if line: c.drawCentredString(bx + bw/2, dy, line.strip())
        # Number badge
        c.setFillColor(clr)
        c.circle(bx + 12, by + 6, 9, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(WHITE)
        c.drawCentredString(bx + 12, by + 3, str(i+1))
        # Arrow
        if i < 3:
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 10)
            c.drawString(bx + bw + 1, by - 55, "→")
    # Key value proposition
    draw_card(c, 40, 100, W-80, 55)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(EMERALD)
    c.drawString(56, 138, "💡  Why Swarms Beat Single-Agent AI")
    bullets = ["Each agent specializes — depth beats breadth", "Sequential context passing = compounding intelligence", "Validator catches errors before they reach you"]
    for i, b in enumerate(bullets):
        c.setFont("Helvetica", 8.5)
        c.setFillColor(MUTED)
        c.drawString(56, 124 - i*12, f"• {b}")
    footer(c, 3)
    c.showPage()

def slide4_architecture(c):
    draw_bg(c, INDIGO)
    accent_bar(c)
    slide_label(c, "03 — Architecture Diagram")
    slide_title(c, "System Architecture", y=H-65, size=26)
    # Architecture diagram
    # Frontend box
    fw = 140; fh = 100; fx = 30; fy = H-200
    draw_card(c, fx, fy-fh, fw, fh, CYAN)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(CYAN); c.drawCentredString(fx+fw/2, fy-18, "FRONTEND")
    c.setFont("Helvetica", 8); c.setFillColor(MUTED)
    for i, t in enumerate(["HTML5 / CSS3", "Vanilla JS", "SSE Client", "Fetch API"]):
        c.drawCentredString(fx+fw/2, fy-34-i*12, t)
    # FastAPI box
    aw = 150; ah = 120; ax = 200; ay = H-185
    draw_card(c, ax, ay-ah, aw, ah, INDIGO)
    c.setFont("Helvetica-Bold", 9); c.setFillColor(INDIGO)
    c.drawCentredString(ax+aw/2, ay-18, "FASTAPI BACKEND")
    c.setFont("Helvetica", 8); c.setFillColor(MUTED)
    for i, t in enumerate(["Python 3.11", "Agent Orchestrator", "SSE Streaming", "/api/swarm/stream", "Jinja2 Templates"]):
        c.drawCentredString(ax+aw/2, ay-34-i*12, t)
    # Agent Swarm box
    sw = 160; sh = 140; sx = 380; sy = H-175
    draw_card(c, sx, sy-sh, sw, sh, EMERALD)
    c.setFont("Helvetica-Bold", 9); c.setFillColor(EMERALD)
    c.drawCentredString(sx+sw/2, sy-18, "AGENT SWARM")
    for i, (ic, nm, cl) in enumerate([("🗺️","Planner",INDIGO),("🔍","Researcher",CYAN),("✍️","Writer",EMERALD),("✅","Validator",AMBER)]):
        c.setFillColor(cl); c.setFont("Helvetica", 8.5)
        c.drawString(sx+14, sy-36-i*22, f"{ic} {nm} Agent")
    # OpenAI box
    ow = 130; oh = 60; ox = W-170; oy = H-215
    draw_card(c, ox, oy-oh, ow, oh, AMBER)
    c.setFont("Helvetica-Bold", 9); c.setFillColor(AMBER)
    c.drawCentredString(ox+ow/2, oy-18, "AZURE OPENAI")
    c.setFont("Helvetica", 8); c.setFillColor(MUTED)
    c.drawCentredString(ox+ow/2, oy-34, "GPT-4o-mini")
    c.drawCentredString(ox+ow/2, oy-48, "gpt-4o-mini model")
    # Arrows
    c.setStrokeColor(MUTED); c.setLineWidth(1)
    c.line(fx+fw, fy-fh/2, ax, ay-ah/2)
    c.line(ax+aw, ay-ah/2, sx, sy-sh/2)
    c.line(sx+sw, sy-sh/2, ox, oy-oh/2)
    # Arrow heads - use path drawing
    for (ex, ey) in [(ax, ay-ah/2), (sx, sy-sh/2), (ox, oy-oh/2)]:
        c.setFillColor(MUTED)
        p = c.beginPath()
        p.moveTo(ex, ey)
        p.lineTo(ex-8, ey-4)
        p.lineTo(ex-8, ey+4)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
    # Request/Response labels
    c.setFont("Helvetica", 7); c.setFillColor(DIM)
    c.drawString(fx+fw+5, fy-fh/2+5, "HTTP/SSE")
    c.drawString(ax+aw+5, ay-ah/2+5, "Agent msgs")
    c.drawString(sx+sw+5, sy-sh/2+5, "API calls")
    # Flow description
    draw_card(c, 30, 80, W-60, 55)
    c.setFont("Helvetica-Bold", 9); c.setFillColor(WHITE)
    c.drawString(46, 118, "Request Flow")
    c.setFont("Helvetica", 8.5); c.setFillColor(MUTED)
    c.drawString(46, 104, "User types task  →  POST /api/swarm/stream  →  Agents run in sequence  →  SSE chunks stream back in real-time")
    c.drawString(46, 90, "Each agent receives full conversation history  →  Context compounds  →  Validator delivers final output")
    footer(c, 4)
    c.showPage()

def slide5_ai_integration(c):
    draw_bg(c, AMBER)
    accent_bar(c, AMBER)
    slide_label(c, "04 — AI Integration Details", AMBER)
    slide_title(c, "Azure OpenAI Integration", y=H-65, size=26)
    # Main integration card
    draw_card(c, 40, H-210, W-80, 110)
    c.setFont("Helvetica-Bold", 10); c.setFillColor(AMBER)
    c.drawString(56, H-108, "⚡  OpenAI Python SDK → Azure OpenAI Service")
    details = [
        ("Model", "GPT-4o-mini (Azure OpenAI deployment)"),
        ("Endpoint", "Azure OpenAI Service via OpenAI client"),
        ("Max Tokens", "800 per agent call · 3,200 total per swarm run"),
        ("Streaming", "Server-Sent Events (SSE) for real-time UI updates"),
    ]
    for i, (k, v) in enumerate(details):
        c.setFont("Helvetica-Bold", 9); c.setFillColor(WHITE)
        c.drawString(56, H-128 - i*16, f"{k}:")
        c.setFont("Helvetica", 9); c.setFillColor(MUTED)
        c.drawString(130, H-128 - i*16, v)
    # System prompt strategy
    draw_card(c, 40, H-360, W-80, 130)
    c.setFont("Helvetica-Bold", 10); c.setFillColor(CYAN)
    c.drawString(56, H-238, "🧠  System Prompt Engineering Strategy")
    strategies = [
        ("Role Isolation", "Each agent has a strict system prompt defining its sole responsibility and output format."),
        ("Context Chaining", "Every agent receives prior agents' outputs in the conversation history."),
        ("Output Contracts", "Agents output structured sections (PLAN:, RESEARCH FINDINGS:, DELIVERABLE:, etc.)"),
        ("Temperature", "0.7 — balances creativity with consistency across all agent calls."),
    ]
    for i, (k, v) in enumerate(strategies):
        c.setFont("Helvetica-Bold", 8.5); c.setFillColor(EMERALD)
        c.drawString(56, H-258-i*18, f"• {k}:")
        c.setFont("Helvetica", 8.5); c.setFillColor(MUTED)
        c.drawString(130, H-258-i*18, v)
    # Endpoints used
    draw_card(c, 40, 80, W-80, 60)
    c.setFont("Helvetica-Bold", 9); c.setFillColor(WHITE)
    c.drawString(56, 124, "API Endpoints")
    endpoints = ["POST  /api/swarm/stream  — SSE streaming run", "POST  /api/swarm/run  — Synchronous JSON run", "GET   /agents  — Agent metadata"]
    for i, ep in enumerate(endpoints):
        c.setFont("Courier", 8); c.setFillColor(CYAN)
        c.drawString(56, 110 - i*12, ep)
    footer(c, 5)
    c.showPage()

def slide6_demo(c):
    draw_bg(c, CYAN)
    accent_bar(c, CYAN)
    slide_label(c, "05 — Demo Screenshots", CYAN)
    slide_title(c, "Live Prototype Walkthrough", y=H-65, size=26)
    slide_subtitle(c, "Real-time streaming UI showing all four agents collaborating on a complex task.", y=H-90)
    screens = [
        ("🏠  Hero & Input", "Dark space-themed UI with hexagonal motif. Task textarea + optional context field. Six example prompts for instant testing."),
        ("⬡  Agent Pipeline", "Four agent cards render live as they run — each streams token-by-token output in real-time via SSE."),
        ("✅  Final Output", "Validated final result panel with copy to clipboard and download as .txt functionality."),
        ("📱  Responsive", "Fully responsive design — works on mobile, tablet, and desktop."),
    ]
    sw_card = (W - 80 - 15) / 2; sh_card = 100
    for i, (title, desc) in enumerate(screens):
        col = i % 2; row = i // 2
        cx = 40 + col * (sw_card + 15)
        cy = H - 115 - row * (sh_card + 15)
        draw_card(c, cx, cy - sh_card, sw_card, sh_card)
        c.setFont("Helvetica-Bold", 9.5); c.setFillColor(CYAN)
        c.drawString(cx+14, cy-22, title)
        c.setFont("Helvetica", 8.5); c.setFillColor(MUTED)
        words = desc.split()
        line = ""; dy = cy-38
        for word in words:
            test = line + word + " "
            if c.stringWidth(test, "Helvetica", 8.5) > sw_card-28:
                c.drawString(cx+14, dy, line.strip()); line = word+" "; dy-=13
            else:
                line = test
        if line: c.drawString(cx+14, dy, line.strip())
    # Live link
    draw_card(c, 40, 80, W-80, 55)
    c.setFont("Helvetica-Bold", 10); c.setFillColor(CYAN)
    c.drawString(56, 118, "🌐  Live Deployment")
    c.setFont("Helvetica", 9); c.setFillColor(MUTED)
    c.drawString(56, 104, "Deployed on Render.com (free tier) · Accessible at public HTTPS URL · Stays live 30+ days post-deadline")
    c.setFont("Courier-Bold", 9); c.setFillColor(WHITE)
    c.drawString(56, 90, "https://swarmdesk.onrender.com")
    footer(c, 6)
    c.showPage()

def slide7_use_cases(c):
    draw_bg(c, EMERALD)
    accent_bar(c, EMERALD)
    slide_label(c, "06 — Use Cases", EMERALD)
    slide_title(c, "What SwarmDesk can do for you", y=H-65, size=26)
    use_cases = [
        ("📄", "Project Proposals", "Full proposals with exec summary, technical approach, timeline, and risk assessment"),
        ("🏃", "Sprint Planning", "Complete sprint plans with story breakdowns, assignments, velocity estimates"),
        ("📊", "Competitive Analysis", "Market positioning, feature comparisons, strategic recommendations"),
        ("🏗️", "Technical Architecture", "System design docs with diagrams, tech stack rationale, trade-off analysis"),
        ("📧", "Team Communications", "Status emails, stakeholder updates, meeting summaries with action items"),
        ("⚠️", "Risk Assessments", "Comprehensive risk registers with likelihood, impact, and mitigation strategies"),
    ]
    uc_w = (W - 80 - 20) / 3; uc_h = 105
    for i, (icon, title, desc) in enumerate(use_cases):
        col = i % 3; row = i // 2
        cx = 40 + col * (uc_w + 10)
        cy = H - 115 - row * (uc_h + 12)
        draw_card(c, cx, cy - uc_h, uc_w, uc_h)
        c.setFont("Helvetica-Bold", 18); c.setFillColor(WHITE)
        c.drawString(cx+12, cy-28, icon)
        c.setFont("Helvetica-Bold", 9); c.setFillColor(EMERALD)
        c.drawString(cx+12, cy-46, title)
        c.setFont("Helvetica", 8); c.setFillColor(MUTED)
        words = desc.split()
        line = ""; dy = cy-62
        for word in words:
            test = line + word + " "
            if c.stringWidth(test, "Helvetica", 8) > uc_w-24:
                c.drawString(cx+12, dy, line.strip()); line = word+" "; dy-=12
            else:
                line = test
        if line: c.drawString(cx+12, dy, line.strip())
    footer(c, 7)
    c.showPage()

def slide8_tech_stack(c):
    draw_bg(c, INDIGO)
    accent_bar(c)
    slide_label(c, "07 — Tech Stack & Microsoft AI")
    slide_title(c, "Built on the Microsoft AI Stack", y=H-65, size=26)
    # Microsoft AI stack highlight
    draw_card(c, 40, H-175, W-80, 80, INDIGO)
    c.setFont("Helvetica-Bold", 11); c.setFillColor(INDIGO)
    c.drawString(56, H-108, "⚡  Microsoft AI Integration")
    c.setFont("Helvetica", 9); c.setFillColor(MUTED)
    c.drawString(56, H-124, "Azure OpenAI Service powers all four agents via the GPT-4o-mini deployment.")
    c.drawString(56, H-140, "GitHub Copilot used throughout development for code completion and review.")
    c.drawString(56, H-156, "Deployed to Azure-compatible infrastructure (Render.com with Azure-compatible endpoints).")
    # Full stack table
    stack = [
        ("Backend Framework", "FastAPI 0.115", "Modern, async-first Python web framework"),
        ("Language", "Python 3.11", "Type hints, async/await throughout"),
        ("AI Service", "Azure OpenAI / GPT-4o-mini", "4 parallel agent calls per swarm run"),
        ("Streaming", "Server-Sent Events (SSE)", "Real-time token streaming to browser"),
        ("Templates", "Jinja2", "Server-side HTML rendering"),
        ("Frontend", "HTML5, CSS3, Vanilla JS", "Zero framework dependencies"),
        ("Typography", "Space Grotesk + Inter", "Google Fonts — professional UI"),
        ("Deployment", "Render.com", "Free tier — HTTPS, auto-deploy from GitHub"),
        ("Dev Tooling", "GitHub Copilot", "AI-assisted development (disclosed)"),
    ]
    row_h = 22; t_y = H-200
    draw_card(c, 40, t_y - len(stack)*row_h - 10, W-80, len(stack)*row_h + 30)
    for i, (cat, tech, note) in enumerate(stack):
        ry = t_y - 5 - i * row_h
        if i % 2 == 0:
            c.setFillColor(colors.HexColor("#141e2e")); c.setFillAlpha(0.5)
            c.rect(41, ry-row_h+4, W-82, row_h-2, fill=1, stroke=0)
            c.setFillAlpha(1.0)
        c.setFont("Helvetica-Bold", 8); c.setFillColor(WHITE)
        c.drawString(55, ry-10, cat)
        c.setFont("Helvetica", 8); c.setFillColor(CYAN)
        c.drawString(200, ry-10, tech)
        c.setFont("Helvetica", 8); c.setFillColor(MUTED)
        c.drawString(360, ry-10, note)
    footer(c, 8)
    c.showPage()

def slide9_team(c):
    draw_bg(c, AMBER)
    accent_bar(c, AMBER)
    slide_label(c, "08 — Team Introduction", AMBER)
    slide_title(c, "The Team", y=H-65, size=26)
    # Team member card
    tm_w = W - 80; tm_h = 130
    draw_card(c, 40, H-230, tm_w, tm_h, AMBER)
    c.setFont("Helvetica-Bold", 40); c.setFillColor(AMBER)
    c.drawString(60, H-148, "👤")
    c.setFont("Helvetica-Bold", 16); c.setFillColor(WHITE)
    c.drawString(120, H-128, "[Your Name]")
    c.setFont("Helvetica-Bold", 10); c.setFillColor(AMBER)
    c.drawString(120, H-148, "Full-Stack AI Engineer · Hackathon Solo Participant")
    skills_row = ["Python", "FastAPI", "GenAI", "AI Agents", "Azure OpenAI", "HTML/CSS", "AI Engineering"]
    sx = 120
    for skill in skills_row:
        sw = c.stringWidth(skill, "Helvetica-Bold", 8) + 14
        c.setFillColor(AMBER); c.setFillAlpha(0.15)
        c.roundRect(sx, H-172, sw, 16, 4, fill=1, stroke=0)
        c.setFillAlpha(1.0)
        c.setStrokeColor(AMBER); c.setLineWidth(0.8)
        c.roundRect(sx, H-172, sw, 16, 4, fill=0, stroke=1)
        c.setFont("Helvetica-Bold", 8); c.setFillColor(AMBER)
        c.drawString(sx+7, H-164, skill)
        sx += sw + 6
    # AI Tools Disclosure
    draw_card(c, 40, H-370, W-80, 110)
    c.setFont("Helvetica-Bold", 10); c.setFillColor(CYAN)
    c.drawString(56, H-268, "🤖  AI Tools Disclosure (Required)")
    disclosures = [
        ("GitHub Copilot", "Code completion, docstring generation, boilerplate acceleration during development"),
        ("Claude (Anthropic)", "Architecture design brainstorming, code review, documentation assistance"),
        ("OpenAI GPT-4o-mini", "Production AI runtime — powers all 4 agents in the live application"),
    ]
    for i, (tool, usage) in enumerate(disclosures):
        c.setFont("Helvetica-Bold", 9); c.setFillColor(WHITE)
        c.drawString(56, H-290-i*20, f"• {tool}:")
        c.setFont("Helvetica", 9); c.setFillColor(MUTED)
        c.drawString(175, H-290-i*20, usage)
    c.setFont("Helvetica", 8.5); c.setFillColor(DIM)
    c.drawString(56, H-352, "All AI-generated code was reviewed, modified, and validated by the human developer.")
    # Submission info
    draw_card(c, 40, 80, W-80, 55)
    c.setFont("Helvetica-Bold", 9); c.setFillColor(WHITE)
    c.drawString(56, 118, "📦  Submission Deliverables")
    c.setFont("Helvetica", 8.5); c.setFillColor(MUTED)
    c.drawString(56, 104, "✅ Project Deck (PDF)   ✅ Demo Video (MP4)   ✅ GitHub Repository (public)   ✅ Live Prototype URL")
    footer(c, 9)
    c.showPage()

def slide10_closing(c):
    draw_bg(c, INDIGO)
    accent_bar(c)
    # Big hex background
    c.setFont("Helvetica-Bold", 250)
    c.setFillColor(INDIGO); c.setFillAlpha(0.05)
    c.drawString(-40, H//2 - 120, "⬡")
    c.setFillAlpha(1.0)
    slide_label(c, "09 — Why SwarmDesk Wins")
    c.setFont("Helvetica-Bold", 32); c.setFillColor(WHITE)
    c.drawString(40, H-80, "Why SwarmDesk wins")
    wins = [
        ("🏆", "Novel Architecture", "Multi-agent swarm with sequential context passing — not a chatbot wrapper"),
        ("⚡", "Real-Time Streaming", "Judges can watch agents think and collaborate live"),
        ("🔧", "Production-Ready", "FastAPI + proper REST endpoints + Swagger docs + deployment config"),
        ("🎨", "Polished UI", "Custom design system — not a template or Bootstrap default"),
        ("📊", "Broad Impact", "Works for any knowledge worker task: proposals, plans, analysis, comms"),
        ("🔬", "Extensible", "Easy to add new agents, tools, or integrate with enterprise systems"),
    ]
    for i, (icon, title, desc) in enumerate(wins):
        row = i // 2; col = i % 2
        wx = 40 + col * ((W-80-15)/2 + 15)
        wy = H - 120 - row * 80
        draw_card(c, wx, wy-65, (W-80-15)/2, 65)
        c.setFont("Helvetica-Bold", 14); c.setFillColor(WHITE)
        c.drawString(wx+14, wy-22, icon)
        c.setFont("Helvetica-Bold", 9); c.setFillColor(INDIGO)
        c.drawString(wx+36, wy-22, title)
        c.setFont("Helvetica", 8.5); c.setFillColor(MUTED)
        c.drawString(wx+14, wy-40, desc[:65] + ("…" if len(desc)>65 else ""))
    # CTA
    draw_card(c, 40, 80, W-80, 50, INDIGO)
    c.setFont("Helvetica-Bold", 12); c.setFillColor(WHITE)
    c.drawCentredString(W/2, 114, "⬡  SwarmDesk — One task. Four agents. One answer.")
    c.setFont("Helvetica", 9); c.setFillColor(MUTED)
    c.drawCentredString(W/2, 96, "github.com/YOUR_USERNAME/swarmdesk  ·  swarmdesk.onrender.com")
    footer(c, 10)
    c.showPage()

# ── Build PDF ─────────────────────────────────────────────────────────────────

out_path = "/mnt/user-data/outputs/TeamName_Deck.pdf"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

c = canvas.Canvas(out_path, pagesize=A4)
c.setTitle("SwarmDesk — Microsoft AI Hackathon 2026")
c.setAuthor("[Your Name]")
c.setSubject("Multi-Agent AI Productivity System")

slide1_cover(c)
slide2_problem(c)
slide3_solution(c)
slide4_architecture(c)
slide5_ai_integration(c)
slide6_demo(c)
slide7_use_cases(c)
slide8_tech_stack(c)
slide9_team(c)
slide10_closing(c)

c.save()
print(f"PDF saved to: {out_path}")
