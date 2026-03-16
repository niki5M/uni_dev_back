const MASTER_URL = "http://127.0.0.1:9000";

function getLoadClass(load) {
  if (load < 0) return "offline";
  if (load <= 3) return "low";
  if (load <= 7) return "medium";
  return "high";
}

function renderNodeCell(nodeId) {
  const group = nodeId.split("_")[0]; // worker_8001 -> worker
  return `
    <div class="pill-node">
      <span>${group}</span>
      <strong>${nodeId}</strong>
    </div>
  `;
}

function renderLoadCell(load) {
  if (load < 0) {
    return `
      <div class="pill-load offline">
        недоступен
      </div>
    `;
  }
  const cls = getLoadClass(load);
  let label = "";
  if (cls === "low") label = "низкая";
  else if (cls === "medium") label = "средняя";
  else if (cls === "high") label = "высокая";
  return `
    <div class="pill-load ${cls}">
      <span>${load}</span>
      <span>${label}</span>
    </div>
  `;
}

function updateTableFromLoads(loads, tableId) {
  const tableBody = document.getElementById(tableId);
  if (!tableBody) return;
  tableBody.innerHTML = "";

  // Показываем только воркеров (листья дерева)
  const entries = Object.entries(loads).filter(([id]) => id.startsWith("worker_"));

  if (entries.length === 0) {
    const row = document.createElement("tr");
    row.innerHTML = `<td colspan="2">Нет данных о воркерах</td>`;
    tableBody.appendChild(row);
    return;
  }

  for (const [nodeId, load] of entries) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${renderNodeCell(nodeId)}</td>
      <td>${renderLoadCell(load)}</td>
    `;
    tableBody.appendChild(row);
  }
}

function setTreeView(text) {
  const treeEl = document.getElementById("treeView");
  if (!treeEl) return;
  treeEl.textContent = text;
}

function fetchStatus() {
  fetch(`${MASTER_URL}/visualize`)
    .then(r => {
      if (!r.ok) {
        throw new Error(`HTTP ${r.status}`);
      }
      return r.json();
    })
    .then(data => {
      updateTableFromLoads(data.loads || {}, "beforeBalance");
      setTreeView("Текущая топология и нагрузки:\n\n" + (data.tree || ""));
    })
    .catch(err => {
      console.error(err);
      setTreeView(
        "Ошибка при получении состояния от мастера.\n" +
        "Убедитесь, что запущены мастер, группы и воркеры.\n\n" +
        "Подробности смотрите в консоли браузера."
      );
    });
}

function balanceOnce() {
  fetch(`${MASTER_URL}/balance`)
    .then(() => fetch(`${MASTER_URL}/visualize`))
    .then(r => {
      if (!r.ok) {
        throw new Error(`HTTP ${r.status}`);
      }
      return r.json();
    })
    .then(data => {
      updateTableFromLoads(data.loads || {}, "afterBalance");
      setTreeView(
        "Текущая топология и нагрузки (после балансировки):\n\n" +
        (data.tree || "")
      );
    })
    .catch(err => {
      console.error(err);
      setTreeView(
        "Ошибка при выполнении балансировки или получении состояния.\n" +
        "Проверьте, что мастер доступен по адресу http://127.0.0.1:9000.\n\n" +
        "Подробности смотрите в консоли браузера."
      );
    });
}

window.onload = fetchStatus;

