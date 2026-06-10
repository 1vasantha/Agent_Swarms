// ── SwarmDesk Frontend App ─────────────────────────────────────────────────
// Handles: Agent display, SSE streaming, UI state, copy/download

const API_BASE = window.location.origin;

// Agent color map
const AGENT_COLORS = {
  planner:    '#6366f1',
  researcher: '#06b6d4',
  writer:     '#10b981',
  validator:  '#f59e0b'
};

// State
let swarmRunning = false;
let timerInterval = null;
let startTime = null;
let agentOutputs = {};
let currentTask = '';

// ── Init ───────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  checkHealth();
  loadAgents();
  loadExamples();
  setupCharCounter();
});

// ── Health Check ───────────────────────────────────────────────────────────

async function checkHealth() {
  const dot  = document.getElementById('statusDot');
  const text = document.getElementById('statusText');
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (res.ok) {
      dot.className  = 'status-dot online';
      text.textContent = 'API Online';
    } else {
      throw new Error('not ok');
    }
  } catch {
    dot.className  = 'status-dot error';
    text.textContent = 'API Offline';
  }
}

// ── Load Agents ────────────────────────────────────────────────────────────

async function loadAgents() {
  try {
    const res  = await fetch(`${API_BASE}/agents`);
    const data = await res.json();
    renderAgents(data.agents);
  } catch (e) {
    console.error('Failed to load agents', e);
  }
}

const AGENT_DESCS = {
  planner:    'Deconstructs your task into a precise, actionable plan — assigning scope, sequence, and ownership before a single word is written.',
  researcher: 'Mines domain knowledge, frameworks, and current best-practices to supply the Writer with everything it needs to produce expert output.',
  writer:     'Synthesizes the plan and research into a polished, ready-to-use deliverable — report, email, strategy doc, code, or whatever you need.',
  validator:  'Scrutinizes the Writer\'s output for accuracy, completeness, and quality — scoring it and delivering an improved final version.'
};

function renderAgents(agents) {
  const grid = document.getElementById('agentsGrid');
  grid.innerHTML = agents.map(a => `
    <div class="agent-card" style="border-left: 3px solid ${a.color}20; border-color: ${a.color}25">
      <div class="agent-card-icon">${a.icon}</div>
      <div class="agent-card-name">${a.name}</div>
      <div class="agent-card-role" style="color:${a.color}">${a.role}</div>
      <div class="agent-card-desc">${AGENT_DESCS[a.id] || ''}</div>
    </div>
  `).join('');
}

// ── Load Examples ──────────────────────────────────────────────────────────

async function loadExamples() {
  try {
    const res  = await fetch(`${API_BASE}/api/examples`);
    const data = await res.json();
    renderExamples(data.examples);
  } catch (e) {
    console.error('Failed to load examples', e);
  }
}

function renderExamples(examples) {
  const grid = document.getElementById('examplesGrid');
  grid.innerHTML = examples.map(ex => `
    <div class="example-card" onclick="useExample(${JSON.stringify(ex.task).replace(/'/g, "&#39;")})">
      <div class="example-card-icon">${ex.icon}</div>
      <div>
        <div class="example-card-title">${ex.title}</div>
        <div class="example-card-task">${ex.task.substring(0, 90)}…</div>
      </div>
    </div>
  `).join('');
}

function useExample(task) {
  document.getElementById('taskInput').value = task;
  updateCharCount();
  document.getElementById('workspace').scrollIntoView({ behavior: 'smooth' });
  setTimeout(() => document.getElementById('taskInput').focus(), 500);
}

// ── Char Counter ───────────────────────────────────────────────────────────

function setupCharCounter() {
  const ta = document.getElementById('taskInput');
  ta.addEventListener('input', updateCharCount);
}

function updateCharCount() {
  const ta  = document.getElementById('taskInput');
  const el  = document.getElementById('charCount');
  const len = ta.value.length;
  el.textContent = `${len} / 1000`;
  el.style.color = len > 900 ? '#f43f5e' : len > 700 ? '#f59e0b' : '';
}

// ── Run Swarm ──────────────────────────────────────────────────────────────

async function runSwarm() {
  const taskInput    = document.getElementById('taskInput');
  const contextInput = document.getElementById('contextInput');
  const task         = taskInput.value.trim();
  const context      = contextInput.value.trim();

  if (!task) {
    taskInput.focus();
    taskInput.style.borderColor = '#f43f5e';
    setTimeout(() => taskInput.style.borderColor = '', 1500);
    return;
  }

  if (swarmRunning) return;

  currentTask = task;
  swarmRunning = true;
  agentOutputs = {};

  // UI changes
  const btn = document.getElementById('runBtn');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> Swarm Running…`;

  // Show output section
  const outputEl = document.getElementById('swarmOutput');
  outputEl.classList.remove('hidden');
  document.getElementById('outputStatus').textContent = 'Swarm initializing…';
  document.getElementById('agentPanels').innerHTML = '';
  document.getElementById('finalResult').classList.add('hidden');
  document.getElementById('finalContent').textContent = '';
  document.getElementById('swarmStats').innerHTML = '';

  outputEl.scrollIntoView({ behavior: 'smooth', block: 'start' });

  // Start timer
  startTime = Date.now();
  timerInterval = setInterval(() => {
    document.getElementById('elapsedTime').textContent =
      ((Date.now() - startTime) / 1000).toFixed(1) + 's';
  }, 100);

  // SSE stream
  try {
    const response = await fetch(`${API_BASE}/api/swarm/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task, context })
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const reader  = response.body.getReader();
    console.log(response,"renderrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    const decoder = new TextDecoder();
    let buffer    = '';

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop();

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        try {
          const event = JSON.parse(line.slice(6));
          handleEvent(event);
        } catch {}
      }
    }
  } catch (err) {
    document.getElementById('outputStatus').textContent = '⚠️ Error: ' + err.message;
    console.error(err);
  } finally {
    clearInterval(timerInterval);
    swarmRunning = false;
    btn.disabled = false;
    btn.innerHTML = `<span class="run-btn-icon">⬡</span> Dispatch Swarm`;
  }
}

// ── Event Handler ──────────────────────────────────────────────────────────

function handleEvent(event) {
  switch (event.type) {

    case 'agent_start': {
      document.getElementById('outputStatus').textContent =
        `${event.icon} ${event.name} is working…`;
      createAgentPanel(event.agent, event.name, event.icon, event.color);
      break;
    }

    case 'agent_chunk': {
      const bodyEl = document.getElementById(`panel-body-${event.agent}`);
      if (bodyEl) {
        agentOutputs[event.agent] = (agentOutputs[event.agent] || '') + event.chunk;
        bodyEl.textContent = agentOutputs[event.agent];
        bodyEl.classList.add('typing-cursor');
      }
      break;
    }

    case 'agent_done': {
      agentOutputs[event.agent] = event.output;
      const bodyEl   = document.getElementById(`panel-body-${event.agent}`);
      const statusEl = document.getElementById(`panel-status-${event.agent}`);
      const durEl    = document.getElementById(`panel-dur-${event.agent}`);
      const panelEl  = document.getElementById(`panel-${event.agent}`);

      if (bodyEl)   { bodyEl.textContent = event.output; bodyEl.classList.remove('typing-cursor'); }
      if (statusEl) { statusEl.textContent = 'Done'; statusEl.className = 'panel-status done'; }
      if (durEl)    { durEl.textContent = event.duration + 's'; }
      if (panelEl)  { panelEl.className = 'agent-panel done'; }
      break;
    }

    case 'agent_error': {
      const statusEl = document.getElementById(`panel-status-${event.agent}`);
      if (statusEl) { statusEl.textContent = 'Error'; statusEl.className = 'panel-status'; statusEl.style.color = '#f43f5e'; }
      break;
    }

    case 'swarm_complete': {
      document.getElementById('outputStatus').textContent = '✅ Swarm complete';
      showFinalResult();
      break;
    }
  }
}

// ── Create Agent Panel ─────────────────────────────────────────────────────

function createAgentPanel(agentId, name, icon, color) {
  const panels = document.getElementById('agentPanels');
  const div    = document.createElement('div');
  div.id        = `panel-${agentId}`;
  div.className = 'agent-panel active';
  div.innerHTML = `
    <div class="panel-header" onclick="togglePanel('${agentId}')">
      <span class="panel-icon">${icon}</span>
      <span class="panel-name" style="color:${color}">${name}</span>
      <span class="panel-status running" id="panel-status-${agentId}">Running</span>
      <span class="panel-duration" id="panel-dur-${agentId}"></span>
    </div>
    <div class="panel-body" id="panel-body-${agentId}"></div>
  `;
  panels.appendChild(div);
  div.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function togglePanel(agentId) {
  const body = document.getElementById(`panel-body-${agentId}`);
  if (body) body.classList.toggle('collapsed');
}

// ── Final Result ───────────────────────────────────────────────────────────

function showFinalResult() {
  const validatorOutput = agentOutputs['validator'] || '';
  // Extract final output section
  let finalContent = validatorOutput;
  const match = validatorOutput.match(/FINAL OUTPUT:([\s\S]*)/i);
  if (match) finalContent = match[1].trim();

  document.getElementById('finalContent').textContent = finalContent;

  // Stats
  const totalTime = ((Date.now() - startTime) / 1000).toFixed(1);
  const agentCount = Object.keys(agentOutputs).length;
  document.getElementById('swarmStats').innerHTML = `
    <div class="stat-item"><span class="stat-label">Total time:</span><span class="stat-value">${totalTime}s</span></div>
    <div class="stat-item"><span class="stat-label">Agents used:</span><span class="stat-value">${agentCount}</span></div>
    <div class="stat-item"><span class="stat-label">Task:</span><span class="stat-value">${currentTask.substring(0, 50)}${currentTask.length > 50 ? '…' : ''}</span></div>
    <div class="stat-item"><span class="stat-label">Model:</span><span class="stat-value">GPT-4o-mini</span></div>
  `;

  document.getElementById('finalResult').classList.remove('hidden');
  document.getElementById('finalResult').scrollIntoView({ behavior: 'smooth' });
}

// ── Actions ────────────────────────────────────────────────────────────────

function copyFinal() {
  const content = document.getElementById('finalContent').textContent;
  navigator.clipboard.writeText(content).then(() => {
    const btn = event.target;
    const orig = btn.textContent;
    btn.textContent = '✓ Copied!';
    setTimeout(() => btn.textContent = orig, 2000);
  });
}

function downloadFinal() {
  const content = document.getElementById('finalContent').textContent;
  const blob = new Blob([content], { type: 'text/plain' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = 'swarmdesk-output.txt';
  a.click();
  URL.revokeObjectURL(url);
}

function clearOutput() {
  document.getElementById('swarmOutput').classList.add('hidden');
  agentOutputs = {};
  currentTask  = '';
}
