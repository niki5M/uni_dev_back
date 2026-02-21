# -*- coding: utf-8 -*-
"""
Промежуточный узел (Group) для алгоритма "Эхо".
Получает маркер от родителя, отправляет детям, собирает эхо и возвращает родителю.
"""
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
from balancer.config import TREE, get_node_url
import httpx
import asyncio

# NODE_ID определяется через переменную окружения или по порту при запуске через main()
NODE_ID = os.environ.get("GROUP_NODE_ID", "group_A")

app = FastAPI(title="Group Node")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class EchoTokenBody(BaseModel):
    from_node: str


@app.post("/echo_token")
async def echo_token(body: EchoTokenBody):
    """
    Алгоритм "Эхо": получить маркер от родителя, отправить детям, собрать эхо, вернуть родителю.
    Процесс для не-инициатора из задания.
    """
    from_node = body.from_node
    node_info = TREE.get(NODE_ID)
    if not node_info:
        raise HTTPException(status_code=404, detail=f"Node {NODE_ID} not found")
    
    children = node_info["children"]
    if not children:
        # Лист (не должно быть для группы, но на всякий случай)
        return {"loads": {}, "status": "echo"}
    
    # Отправить маркер всем детям (кроме from_node, но from_node - это родитель, не ребёнок)
    child_loads = {}
    async with httpx.AsyncClient(timeout=5.0) as client:
        tasks = []
        for child_id in children:
            url = f"{get_node_url(child_id)}/echo_token"
            tasks.append(client.post(url, json={"from_node": NODE_ID}))
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for child_id, resp in zip(children, responses):
            if isinstance(resp, Exception) or resp.status_code != 200:
                child_loads[child_id] = -1
            else:
                data = resp.json()
                child_loads.update(data.get("loads", {}))
    
    return {"loads": child_loads, "status": "echo"}


@app.get("/health")
def health():
    return {"status": "ok", "node_id": NODE_ID, "type": "group"}


def main():
    global NODE_ID
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True, help="Порт узла, например 9001")
    args = parser.parse_args()
    # Определить NODE_ID по порту
    for node_id, info in TREE.items():
        if info.get("port") == args.port and info.get("type") == "intermediate":
            NODE_ID = node_id
            break
    uvicorn.run(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
