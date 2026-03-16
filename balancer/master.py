# -*- coding: utf-8 -*-

# Центральный узел (Master). 
import asyncio
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from balancer.config import TREE, get_worker_url, MASTER_PORT, get_all_workers
from balancer.echo_algorithm import echo_algorithm_collect_load, collect_load_from_workers
from balancer.finn_algorithm import run_finn_algorithm

# Текущая карта нагрузок (обновляется волной)
load_map: dict = {}
# Хост воркеров (для перераспределения)
BALANCER_HOST = "127.0.0.1"
INTERVAL_SEC = 5
REBALANCE_THRESHOLD = 2  # перераспределять, если разница >= 2


async def run_wave_and_rebalance():
    """Периодически: волна сбора нагрузки + решение о перераспределении."""
    global load_map
    while True:
        try:
            load_map = await collect_load_from_workers(BALANCER_HOST)
            # Решение: найти max и min (игнорируем недоступные -1)
            valid = {k: v for k, v in load_map.items() if v >= 0}
            if len(valid) < 2:
                await asyncio.sleep(INTERVAL_SEC)
                continue
            max_node = max(valid, key=valid.get)
            min_node = min(valid, key=valid.get)
            max_load = valid[max_node]
            min_load = valid[min_node]
            if max_load - min_load >= REBALANCE_THRESHOLD:
                move_count = (max_load - min_load) // 2
                if move_count <= 0:
                    await asyncio.sleep(INTERVAL_SEC)
                    continue
                target_url = get_worker_url(min_node, BALANCER_HOST)
                source_url = get_worker_url(max_node, BALANCER_HOST)
                async with httpx.AsyncClient(timeout=5.0) as client:
                    await client.post(
                        f"{source_url}/transfer",
                        json={"target_url": target_url, "count": move_count},
                    )
        except Exception:
            pass  # логировать при необходимости
        await asyncio.sleep(INTERVAL_SEC)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(run_wave_and_rebalance())
    yield


app = FastAPI(title="Master (Central Node)", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/tree")
def get_tree():
    """Структура дерева и текущие нагрузки (для визуализации во Flutter)."""
    return JSONResponse({
        "topology": TREE,
        "loads": load_map,
        "master_port": MASTER_PORT,
    })


@app.get("/loads")
def get_loads():
    """Только карта нагрузок (для монитора)."""
    return JSONResponse(load_map)


@app.get("/assign")
def get_least_loaded_worker():
    """
    Вернуть URL наименее загруженного воркера (как в примере с клиникой: куда направить новую задачу).
    Для отчёта: аналог register_patient — размещение новой работы в наименее загруженный узел.
    """
    valid = {k: v for k, v in load_map.items() if v >= 0}
    if not valid:
        return JSONResponse({"error": "Нет доступных воркеров"}, status_code=503)
    min_node = min(valid, key=valid.get)
    url = get_worker_url(min_node, BALANCER_HOST)
    return JSONResponse({"worker_id": min_node, "worker_url": url, "load": valid[min_node]})


class RegisterRequest(BaseModel):
    """Тело запроса: тип запроса студента (зачётка, расписание, новости)."""
    request_type: str = "gradebook"  # gradebook | schedule | news


@app.post("/register_request")
@app.post("/register_request/")
async def register_request(body: RegisterRequest):
    """
    Централизованная регистрация запроса (аналог register_patient в примере с клиникой).
    Один запрос к мастеру: мастер выбирает наименее загруженный воркер и сам перенаправляет туда задачу.
    """
    valid = {k: v for k, v in load_map.items() if v >= 0}
    if not valid:
        return JSONResponse(
            {"status": "error", "message": "Нет доступных воркеров"},
            status_code=503
        )
    min_node = min(valid, key=valid.get)
    worker_url = get_worker_url(min_node, BALANCER_HOST)
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.post(
            f"{worker_url}/tasks",
            json={"type": body.request_type},
        )
        if r.status_code != 200:
            return JSONResponse(
                {"status": "error", "message": f"Воркер {min_node} не принял задачу"},
                status_code=502
            )
    return JSONResponse({
        "status": "success",
        "worker": min_node,
        "message": f"Запрос типа «{body.request_type}» записан в {min_node}",
    })


@app.get("/balance")
async def trigger_balance():
    """
    Ручной запуск балансировки (аналог load_balance.py: GET /balance).
    Один шаг: сбор нагрузок и при необходимости перераспределение задач.
    """
    global load_map
    load_map = await collect_load_from_workers(BALANCER_HOST)
    valid = {k: v for k, v in load_map.items() if v >= 0}
    if len(valid) < 2:
        return JSONResponse({"status": "success", "message": "Балансировка не требуется (мало узлов)"})
    max_node = max(valid, key=valid.get)
    min_node = min(valid, key=valid.get)
    max_load = valid[max_node]
    min_load = valid[min_node]
    if max_load - min_load < REBALANCE_THRESHOLD:
        return JSONResponse({"status": "success", "message": "Балансировка не требуется"})
    move_count = (max_load - min_load) // 2
    target_url = get_worker_url(min_node, BALANCER_HOST)
    source_url = get_worker_url(max_node, BALANCER_HOST)
    async with httpx.AsyncClient(timeout=5.0) as client:
        await client.post(source_url + "/transfer", json={"target_url": target_url, "count": move_count})
    return JSONResponse({
        "status": "success",
        "message": f"Перенаправлено {move_count} задач от {max_node} к {min_node}",
    })


@app.get("/visualize")
def visualize():
    """
    Визуализация дерева с нагрузками (до и после балансировки).
    Возвращает текстовое представление дерева с нагрузками на каждом узле.
    """
    def build_tree_vis(node_id: str, prefix: str = "", is_last: bool = True) -> str:
        """Рекурсивно строит визуализацию дерева."""
        node_info = TREE[node_id]
        load = load_map.get(node_id, -1)
        load_str = f" (нагрузка: {load})" if load >= 0 else " (недоступен)"
        marker = "└── " if is_last else "├── "
        result = f"{prefix}{marker}{node_id}{load_str}\n"
        
        children = node_info["children"]
        if children:
            new_prefix = prefix + ("    " if is_last else "│   ")
            for i, child_id in enumerate(children):
                is_last_child = (i == len(children) - 1)
                result += build_tree_vis(child_id, new_prefix, is_last_child)
        return result
    
    tree_vis = "master (инициатор)\n"
    for i, child_id in enumerate(TREE["master"]["children"]):
        is_last = (i == len(TREE["master"]["children"]) - 1)
        tree_vis += build_tree_vis(child_id, "", is_last)
    
    return JSONResponse({
        "tree": tree_vis,
        "loads": load_map,
        "workers_only": {w: load_map.get(w, -1) for w in get_all_workers()},
    })


@app.get("/health")
def health():
    return {"status": "ok", "role": "master"}


@app.get("/finn")
def run_finn():
    """
    Запуск волнового алгоритма Финна для текущей топологии TREE.
    Возвращает для каждого узла множества Inc(s) и NInc(s).
    Используется на странице визуализации для лабы 7–10.
    """
    raw_result = run_finn_algorithm("master")
    # Преобразуем множества в отсортированные списки, чтобы их можно было сериализовать в JSON
    serializable = {}
    for node_id, sets in raw_result.items():
        inc = sorted(list(sets.get("Inc", [])))
        ninc = sorted(list(sets.get("NInc", [])))
        serializable[node_id] = {"Inc": inc, "NInc": ninc}
    return JSONResponse(serializable)


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=MASTER_PORT)


if __name__ == "__main__":
    main()
