# Центральный узел (Master).
import asyncio
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from balancer.config import TREE, get_worker_url, MASTER_PORT
from balancer.wave import collect_load_from_workers

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


@app.get("/health")
def health():
    return {"status": "ok", "role": "master"}


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=MASTER_PORT)


if __name__ == "__main__":
    main()
