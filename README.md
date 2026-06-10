# ⬡ SwarmDesk — Multi-Agent AI Productivity System

> **Microsoft AI Hackathon 2026 Submission**  
> Theme 05: Agent Swarms · Built 3 May – 30 June 2026

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://python.org)
[![OpenAI](https://img.shields.io/badge/Azure_OpenAI-GPT--4o-412991?logo=openai)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🧠 What is SwarmDesk?

SwarmDesk is an AI-powered productivity platform that orchestrates a **swarm of four specialized AI agents** to tackle complex professional tasks — producing outputs that are dramatically more thorough, accurate, and polished than any single AI call could deliver.

One task goes in. Four agents collaborate. One validated deliverable comes out.

```
  Task Input
     │
     ▼
  🗺️ Planner Agent  ──── Breaks task into a structured plan
     │
     ▼
  🔍 Researcher Agent ── Gathers domain knowledge & insights
     │
     ▼
  ✍️ Writer Agent ──────  Produces the polished deliverable
     │
     ▼
  ✅ Validator Agent ─── Reviews, scores, and improves output
     │
     ▼
  Final Output (validated & ready-to-use)
```

---

## ✨ Features

- **Real-time streaming** — Watch each agent think and respond via Server-Sent Events (SSE)
- **Sequential pipeline** — Agents pass context to each other, building progressively better output
- **Copy & download** — Export the final validated deliverable with one click
- **Example tasks** — Six pre-built prompts to explore capabilities immediately
- **REST API** — Full FastAPI backend with `/docs` Swagger UI and `/api/swarm/run` endpoint
- **Responsive UI** — Works on desktop and mobile, no framework dependencies

---

## 🏗️ Architecture

```
swarmdesk/
├── backend/
│   ├── main.py              # FastAPI app + agent orchestration
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variable template
├── frontend/
│   ├── templates/
│   │   └── index.html       # Jinja2 HTML template
│   └── static/
│       ├── css/style.css    # Custom design system
│       └── js/app.js        # SSE client + UI logic
└── README.md
```

### Tech Stack

| Layer        | Technology                                    |
|--------------|-----------------------------------------------|
| Backend      | Python 3.11, FastAPI, Uvicorn                 |
| AI / LLM     | Azure OpenAI Service (GPT-4o-mini)            |
| Streaming    | Server-Sent Events (SSE)                      |
| Frontend     | HTML5, CSS3 (custom), Vanilla JavaScript      |
| Templates    | Jinja2                                        |
| Fonts        | Space Grotesk, Inter, JetBrains Mono          |
| Deployment   | Render.com (free tier) / Railway / Fly.io     |

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.11+
- An OpenAI API key (or Azure OpenAI endpoint)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/swarmdesk.git
cd swarmdesk
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# or: venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

```env
OPENAI_API_KEY=sk-...
```

### 5. Run the application

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000` in your browser.

---

## 🌐 API Endpoints

| Method | Endpoint              | Description                                      |
|--------|-----------------------|--------------------------------------------------|
| GET    | `/`                   | Serves the SwarmDesk web UI                      |
| GET    | `/health`             | Health check — returns API status                |
| GET    | `/agents`             | Returns the list of available agents             |
| GET    | `/api/examples`       | Returns example tasks                            |
| POST   | `/api/swarm/stream`   | Runs the swarm with SSE streaming                |
| POST   | `/api/swarm/run`      | Runs the swarm and returns all results as JSON   |
| GET    | `/docs`               | Swagger UI — interactive API documentation       |

### Example API Request

```bash
curl -X POST http://localhost:8000/api/swarm/run \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Write a project proposal for an AI inventory management system",
    "context": "B2B SaaS, mid-size retail, 3-person dev team"
  }'
```

---

## 🤖 Agent System

Each agent has a specialized system prompt that defines its role, output format, and constraints:

| Agent       | Role                        | Output Format                          |
|-------------|-----------------------------|----------------------------------------|
| 🗺️ Planner  | Strategic Planning          | Numbered plan + agent assignments      |
| 🔍 Researcher | Information & Analysis    | Bullet-pointed findings & frameworks   |
| ✍️ Writer   | Content & Solution Creation | Full polished deliverable              |
| ✅ Validator | Quality Assurance           | Strengths, improvements, score, final  |

Each agent receives the full conversation history from all previous agents, enabling true collaborative reasoning.

---

## 🛠️ AI Tools Used

This project was built using the following AI tools in development:

- **GitHub Copilot** — Code completion and boilerplate acceleration
- **Claude (Anthropic)** — Architecture design and code review
- **OpenAI GPT-4o-mini** — The runtime AI powering all four agents in production

All AI-generated code was reviewed, modified, and validated by the human developer. The agent orchestration architecture, SSE streaming pipeline, system prompts, and UI design represent original human engineering decisions.

---

## ☁️ Deployment

### Render.com (Recommended — Free)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Add `OPENAI_API_KEY`
5. Deploy — free tier includes 750 hours/month

### Railway (Alternative)

```bash
# Install Railway CLI
npm i -g @railway/cli
railway login
railway init
railway up
```
Set `OPENAI_API_KEY` in Railway dashboard environment variables.

### Fly.io (Alternative)

```bash
fly launch
fly secrets set OPENAI_API_KEY=sk-...
fly deploy
```

---

## 📋 Submission Checklist

- [x] Project started and built during hackathon period (May–June 2026)
- [x] Uses Microsoft AI stack (Azure OpenAI Service)
- [x] Public GitHub repository with comprehensive README
- [x] FastAPI REST API with Swagger docs
- [x] No secrets or API keys committed to source control
- [x] AI tools disclosed in README
- [x] Working prototype with live deployment link
- [x] Architecture diagram included

---

## 👥 Team

| Name              | Role                                    |
|-------------------|-----------------------------------------|
| [Your Name]       | Full-stack Developer, AI Engineer       |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Credits & Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com) — Modern Python web framework
- [OpenAI Python SDK](https://github.com/openai/openai-python) — LLM API client
- [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) — Display typeface
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/) — Monospace typeface
- Microsoft Azure OpenAI Service — AI infrastructure
