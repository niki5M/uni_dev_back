const API_URL = "http://127.0.0.1:8000";

function getLoadClass(load) {
  if (load <= 30) return "low";
  if (load <= 70) return "medium";
  return "high";
}

function renderLoadCell(load) {
  const cls = getLoadClass(load);
  let label = "";
  if (cls === "low") label = "низкая";
  else if (cls === "medium") label = "средняя";
  else if (cls === "high") label = "высокая";
  const pill = cls === "medium" ? "med" : cls;
  return `
    <div class="load-pill pill-${pill}">
      <span>${load}</span>
      <span>${label}</span>
    </div>
  `;
}

function updateTable(data, tableId) {
  const tableBody = document.getElementById(tableId);
  if (!tableBody) return;
  tableBody.innerHTML = "";

  const entries = Object.entries(data);
  if (entries.length === 0) {
    const row = document.createElement("tr");
    row.innerHTML = `<td colspan="3">Нет данных</td>`;
    tableBody.appendChild(row);
    return;
  }

  for (const [branch, info] of entries) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${info.name || branch}</td>
      <td>${info.address}</td>
      <td>${renderLoadCell(info.load)}</td>
    `;
    tableBody.appendChild(row);
  }
}

function fetchStatus() {
  fetch(`${API_URL}/status`)
    .then(r => {
      if (!r.ok) {
        throw new Error(`HTTP ${r.status}`);
      }
      return r.json();
    })
    .then(data => {
      updateTable(data, "beforeBalance");
    })
    .catch(err => {
      console.error(err);
    });
}

function balanceOnce() {
  fetch(`${API_URL}/balance`)
    .then(r => {
      if (!r.ok) {
        throw new Error(`HTTP ${r.status}`);
      }
      return r.json();
    })
    .then(() => fetch(`${API_URL}/status`))
    .then(r => {
      if (!r.ok) {
        throw new Error(`HTTP ${r.status}`);
      }
      return r.json();
    })
    .then(data => {
      updateTable(data, "afterBalance");
    })
    .catch(err => {
      console.error(err);
    });
}

function sendTenRequests() {
  fetch(`${API_URL}/generate_requests`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ count: 10 }),
  })
    .then(r => {
      if (!r.ok) {
        throw new Error(`HTTP ${r.status}`);
      }
      return r.json();
    })
    .then(data => {
      // Обновляем таблицу "До балансировки" текущим состоянием после генерации 10 запросов
      if (data.current) {
        updateTable(data.current, "beforeBalance");
      } else {
        fetchStatus();
      }
    })
    .catch(err => {
      console.error(err);
    });
}

window.onload = fetchStatus;

