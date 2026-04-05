const API_URL =
  window.location.protocol.startsWith("http") ? "" : "http://127.0.0.1:8000";

function getLoadClass(load, avg) {
  if (load <= avg * 0.8) return "low";
  if (load <= avg * 1.2) return "medium";
  return "high";
}

function setMessage(text, isError = false) {
  const el = document.getElementById("messageBox");
  if (!el) return;
  el.textContent = text;
  el.style.color = isError ? "#fca5a5" : "#93c5fd";
}

function formatJsonPretty(obj) {
  return JSON.stringify(obj, null, 2);
}

function normalizeStatusData(data) {
  if (data && data.loads && typeof data.loads === "object") {
    const result = {};
    for (const [nodeId, load] of Object.entries(data.loads)) {
      result[nodeId] = {
        address: `Узел графа ${nodeId}`,
        load: Number(load || 0),
      };
    }
    return result;
  }
  return data || {};
}

function updateTable(data, tableId) {
  const tableBody = document.getElementById(tableId);
  if (!tableBody) return;
  tableBody.innerHTML = "";
  const rows = normalizeStatusData(data);
  for (const branch in rows) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${branch}</td>
      <td>${rows[branch].address ?? "-"}</td>
      <td>${rows[branch].load ?? 0}</td>
    `;
    tableBody.appendChild(row);
  }
}

function renderLoads(loads) {
  const tableBody = document.getElementById("loadsTable");
  if (!tableBody) return;
  tableBody.innerHTML = "";
  const entries = Object.entries(loads || {});
  const total = entries.reduce((sum, [, load]) => sum + Number(load || 0), 0);
  const avg = entries.length ? total / entries.length : 0;

  for (const [nodeId, load] of entries.sort(([a], [b]) => a.localeCompare(b))) {
    const row = document.createElement("tr");
    const cls = getLoadClass(load, avg || 1);
    row.innerHTML = `
      <td><span class="pill-node"><strong>${nodeId}</strong></span></td>
      <td><span class="pill-load ${cls}">${load}</span></td>
    `;
    tableBody.appendChild(row);
  }
  document.getElementById("avgLoad").textContent = avg.toFixed(2);
  document.getElementById("totalLoad").textContent = String(total);
}

function renderTopology(topology) {
  const graphEl = document.getElementById("graphView");
  if (!graphEl) return;
  const lines = [];
  Object.entries(topology || {})
    .sort(([a], [b]) => a.localeCompare(b))
    .forEach(([src, dsts]) => {
      if (!dsts.length) lines.push(`${src} -> (нет исходящих дуг)`);
      else lines.push(`${src} -> ${dsts.join(", ")}`);
    });
  graphEl.textContent = lines.join("\n");
}

async function apiGet(path) {
  const r = await fetch(`${API_URL}${path}`);
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

async function apiPost(path, payload) {
  const r = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!r.ok) {
    const txt = await r.text();
    throw new Error(`HTTP ${r.status}: ${txt}`);
  }
  return r.json();
}

async function refreshStatus() {
  try {
    const data = await apiGet("/status");
    renderTopology(data.topology || {});
    renderLoads(data.loads || {});
    updateTable(data, "beforeBalance");
    document.getElementById("topologyInput").value = formatJsonPretty(data.topology || {});
    document.getElementById("loadsInput").value = formatJsonPretty(data.loads || {});
    setMessage("Состояние обновлено.");
  } catch (err) {
    setMessage(`Ошибка обновления: ${err.message}`, true);
  }
}

async function applyTopology() {
  try {
    const topology = JSON.parse(document.getElementById("topologyInput").value || "{}");
    await apiPost("/topology", { topology });
    setMessage("Топология сохранена.");
    await refreshStatus();
  } catch (err) {
    setMessage(`Ошибка топологии: ${err.message}`, true);
  }
}

async function applyLoads() {
  try {
    const loads = JSON.parse(document.getElementById("loadsInput").value || "{}");
    await apiPost("/loads", { loads });
    setMessage("Нагрузки сохранены.");
    await refreshStatus();
  } catch (err) {
    setMessage(`Ошибка нагрузок: ${err.message}`, true);
  }
}

async function generateRequests() {
  try {
    const count = Number(document.getElementById("requestsCount").value || 10);
    await apiPost("/generate_requests", { count });
    setMessage(`Добавлено запросов: ${count}`);
    await refreshStatus();
  } catch (err) {
    setMessage(`Ошибка генерации: ${err.message}`, true);
  }
}

function renderLastStep(step) {
  const pre = document.getElementById("stepResult");
  if (!pre) return;
  pre.textContent = formatJsonPretty(step);
}

async function runOneStep() {
  try {
    const step = await apiGet("/balance");
    renderLastStep(step);
    setMessage(`Шаг выполнен. Перенесено: ${step.moved_total}`);
    const status = await apiGet("/status");
    renderTopology(status.topology || {});
    renderLoads(status.loads || {});
    updateTable(status, "afterBalance");
  } catch (err) {
    setMessage(`Ошибка шага балансировки: ${err.message}`, true);
  }
}

async function runUntilStable() {
  try {
    const maxSteps = Number(document.getElementById("maxSteps").value || 20);
    const result = await apiPost("/balance/run", { max_steps: maxSteps });
    const last = result.steps?.[result.steps.length - 1] || {};
    renderLastStep(last);
    setMessage(`Стабилизация завершена. Шагов: ${result.steps?.length || 0}`);
    await refreshStatus();
  } catch (err) {
    setMessage(`Ошибка запуска до стабилизации: ${err.message}`, true);
  }
}

window.refreshStatus = refreshStatus;
window.applyTopology = applyTopology;
window.applyLoads = applyLoads;
window.generateRequests = generateRequests;
window.runOneStep = runOneStep;
window.runUntilStable = runUntilStable;
window.updateTable = updateTable;

// Совместимость с примером пользователя
window.fetchStatus = refreshStatus;
window.balanceLoad = runOneStep;

window.onload = refreshStatus;

