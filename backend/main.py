"""
SwarmDesk - Multi-Agent AI Productivity System
FastAPI Backend with Agent Swarm Architecture
"""

import os
import json
import asyncio
import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import uvicorn
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="SwarmDesk API",
    description="Multi-Agent AI Productivity Assistant powered by Agent Swarms",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and templates
BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=str(BASE_DIR.parent / "frontend" / "static")), name="static")
templates = Jinja2Templates(
    directory=str(BASE_DIR.parent / "frontend" / "templates")
)
# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─── Agent Definitions ────────────────────────────────────────────────────────

AGENTS = {
    "planner": {
        "name": "Planner Agent",
        "icon": "🗺️",
        "color": "#6366f1",
        "role": "Strategic Planning Specialist",
        "system_prompt": """You are the Planner Agent in a multi-agent AI swarm called SwarmDesk.
Your role: Analyze the user's task and break it into a clear, structured execution plan.
Output a numbered step-by-step plan that other agents (Researcher, Writer, Validator) will follow.
Be concise, actionable, and specific. Format output as:
PLAN:
1. [Step]
2. [Step]
...
ASSIGNED_TO: [agent names for each step]
Keep your response under 200 words."""
    },
    "researcher": {
        "name": "Researcher Agent",
        "icon": "🔍",
        "color": "#06b6d4",
        "role": "Information & Analysis Specialist",
        "system_prompt": """You are the Researcher Agent in a multi-agent AI swarm called SwarmDesk.
Your role: Given a task and a plan, gather relevant knowledge, facts, frameworks, and insights.
Synthesize information in a structured way that the Writer Agent can use.
Format output as:
RESEARCH FINDINGS:
- Key facts and data points
- Relevant frameworks/approaches
- Important considerations
Keep your response under 300 words."""
    },
    "writer": {
        "name": "Writer Agent",
        "icon": "✍️",
        "color": "#10b981",
        "role": "Content & Solution Specialist",
        "system_prompt": """You are the Writer Agent in a multi-agent AI swarm called SwarmDesk.
Your role: Using the plan and research, produce the actual deliverable — a professional, high-quality output.
Whether it's an email, report, code snippet, proposal, strategy doc, or answer — make it polished and ready to use.
Format output as:
DELIVERABLE:
[The actual content, well-structured and formatted]
Keep your response focused and professional."""
    },
    "validator": {
        "name": "Validator Agent",
        "icon": "✅",
        "color": "#f59e0b",
        "role": "Quality Assurance Specialist",
        "system_prompt": """You are the Validator Agent in a multi-agent AI swarm called SwarmDesk.
Your role: Review the deliverable from the Writer Agent. Check for:
- Accuracy and completeness
- Quality and professionalism
- Alignment with original task
- Any gaps or improvements
Format output as:
VALIDATION REPORT:
✅ Strengths: [what's good]
⚠️ Improvements: [what can be better]
FINAL SCORE: [X/10]
FINAL OUTPUT: [Improved/approved version of the deliverable]"""
    }
}

# ─── Pydantic Models ───────────────────────────────────────────────────────────

class TaskRequest(BaseModel):
    task: str
    context: Optional[str] = ""

class AgentResponse(BaseModel):
    agent: str
    output: str
    duration: float

# ─── Agent Runner ──────────────────────────────────────────────────────────────

async def run_agent(agent_id: str, messages: list) -> tuple[str, float]:
    """Run a single agent and return its output and duration."""
    agent = AGENTS[agent_id]
    start = time.time()
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": agent["system_prompt"]},
            *messages
        ],
        temperature=0.7,
        max_tokens=800
    )
    
    output = response.choices[0].message.content
    duration = round(time.time() - start, 2)
    return output, duration

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "SwarmDesk API", "version": "1.0.0"}

@app.get("/agents")
async def get_agents():
    return {
        "agents": [
            {
                "id": k,
                "name": v["name"],
                "icon": v["icon"],
                "color": v["color"],
                "role": v["role"]
            }
            for k, v in AGENTS.items()
        ]
    }

@app.post("/api/swarm/stream")
async def run_swarm_stream(task_request: TaskRequest):
    """Stream multi-agent swarm execution as Server-Sent Events."""
    
    async def generate():
        task = task_request.task
        context = task_request.context or ""
        
        # Build context string
        full_task = f"TASK: {task}"
        if context:
            full_task += f"\nCONTEXT: {context}"
        
        conversation_history = []
        conversation_history.append({"role": "user", "content": full_task})
        
        agent_order = ["planner", "researcher", "writer", "validator"]
        
        for agent_id in agent_order:
            agent = AGENTS[agent_id]
            
            # Signal agent start
            yield f"data: {json.dumps({'type': 'agent_start', 'agent': agent_id, 'name': agent['name'], 'icon': agent['icon'], 'color': agent['color']})}\n\n"
            await asyncio.sleep(0.1)
            
            try:
                output, duration = await run_agent(agent_id, conversation_history)
                
                # Add agent output to conversation for next agent
                conversation_history.append({
                    "role": "assistant",
                    "content": f"[{agent['name']}]: {output}"
                })
                
                # Stream token by token (word by word simulation)
                words = output.split(" ")
                streamed = ""
                for i, word in enumerate(words):
                    streamed += word + " "
                    if i % 5 == 0 or i == len(words) - 1:
                        yield f"data: {json.dumps({'type': 'agent_chunk', 'agent': agent_id, 'chunk': streamed, 'done': False})}\n\n"
                        await asyncio.sleep(0.02)
                        streamed = ""
                
                yield f"data: {json.dumps({'type': 'agent_done', 'agent': agent_id, 'output': output, 'duration': duration})}\n\n"
                await asyncio.sleep(0.2)
                
            except Exception as e:
                yield f"data: {json.dumps({'type': 'agent_error', 'agent': agent_id, 'error': str(e)})}\n\n"
        
        yield f"data: {json.dumps({'type': 'swarm_complete'})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/api/swarm/run")
async def run_swarm(task_request: TaskRequest):
    """Run the full agent swarm and return all results."""
    task = task_request.task
    context = task_request.context or ""
    
    full_task = f"TASK: {task}"
    if context:
        full_task += f"\nCONTEXT: {context}"
    
    conversation_history = [{"role": "user", "content": full_task}]
    results = []
    
    for agent_id in ["planner", "researcher", "writer", "validator"]:
        agent = AGENTS[agent_id]
        output, duration = await run_agent(agent_id, conversation_history)
        
        conversation_history.append({
            "role": "assistant",
            "content": f"[{agent['name']}]: {output}"
        })
        
        results.append({
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "icon": agent["icon"],
            "output": output,
            "duration": duration
        })
    
    return {"task": task, "results": results, "total_agents": len(results)}


@app.get("/api/examples")
async def get_examples():
    """Return example tasks for the UI."""
    return {
        "examples": [
            {
                "title": "Write a Project Proposal",
                "task": "Write a project proposal for implementing an AI-powered customer support chatbot for an e-commerce company",
                "icon": "📄"
            },
            {
                "title": "Sprint Planning",
                "task": "Plan a 2-week sprint for a 4-person engineering team building a real-time data dashboard",
                "icon": "🏃"
            },
            {
                "title": "Competitive Analysis",
                "task": "Analyze the competitive landscape for a new AI coding assistant tool entering the market in 2025",
                "icon": "📊"
            },
            {
                "title": "Technical Architecture",
                "task": "Design the technical architecture for a scalable multi-tenant SaaS application handling 100k users",
                "icon": "🏗️"
            },
            {
                "title": "Team Standup Email",
                "task": "Draft a weekly team update email summarizing completed features, blockers, and next week priorities for a product team",
                "icon": "📧"
            },
            {
                "title": "Risk Assessment",
                "task": "Perform a risk assessment for migrating a monolithic application to microservices architecture",
                "icon": "⚠️"
            }
        ]
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
