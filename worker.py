"""
Узел-исполнитель (Worker). Хранит очередь «задач» — имитация запросов к API университета.
Умеет отдавать нагрузку и принимать/передавать задачи по команде центра.
"""
import os
import argparse
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from balancer.models import Task
import httpx

app = FastAPI(title="Worker Node")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Очередь задач узла (в памяти)
tasks: List[Task] = []
# NODE_ID задаётся через env WORKER_NODE_ID или при вызове main(port)
NODE_ID = os.environ.get("WORKER_NODE_ID", "worker_8001")


@app.get("/load")
def get_load():
    """Текущая нагрузка узла (число задач). Для волнового алгоритма."""
    return {"node_id": NODE_ID, "load": len(tasks)}


@app.get("/tasks")
def list_tasks():
    """Список задач (для мониторинга)."""
    return {"node_id": NODE_ID, "count": len(tasks), "tasks": [t.model_dump() for t in tasks]}


@app.post("/tasks")
def add_task(task: Task):
    """Добавить одну задачу (имитация входящего запроса)."""
    tasks.append(task)
    return {"node_id": NODE_ID, "load": len(tasks)}


class AcceptTasksBody(BaseModel):
    tasks: List[dict]


@app.post("/tasks/accept")
def accept_tasks(body: AcceptTasksBody):
    """Принять задачи от другого узла (при перераспределении)."""
    for t in body.tasks:
        tasks.append(Task(**t))
    return {"node_id": NODE_ID, "accepted": len(body.tasks), "load": len(tasks)}


class TransferBody(BaseModel):
    target_url: str
    count: int


@app.post("/transfer")
async def transfer_tasks(body: TransferBody):
    """По команде центра: отправить count задач на target_url. Задачи удаляются только после успешной отправки."""
    global tasks
    if body.count <= 0:
        return {"node_id": NODE_ID, "transferred": 0}
    to_send = min(body.count, len(tasks))
    if to_send == 0:
        return {"node_id": NODE_ID, "transferred": 0}
    batch = [tasks[i].model_dump() for i in range(to_send)]
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{body.target_url.rstrip('/')}/tasks/accept", json={"tasks": batch})
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Worker {body.target_url} refused")
    for _ in range(to_send):
        tasks.pop(0)
    return {"node_id": NODE_ID, "transferred": to_send, "load": len(tasks)}


@app.get("/health")
def health():
    return {"status": "ok", "node_id": NODE_ID}


def main():
    global NODE_ID
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True, help="Порт узла, например 8001")
    args = parser.parse_args()
    NODE_ID = f"worker_{args.port}"
    uvicorn.run(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
