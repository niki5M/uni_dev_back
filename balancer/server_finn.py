# -*- coding: utf-8 -*-
"""
Веб-сервер для лабораторной 7–10:
- /status  — вернуть текущую нагрузку узлов сети;
- /balance — выполнить шаг централизованной балансировки на основе волнового алгоритма Финна.

Используется страницей index.html (script.js) как бэкенд.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from balancer.network import NetworkBalancer

app = FastAPI(title="Finn Network Balancer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

balancer = NetworkBalancer()


@app.get("/status")
def get_status():
    """Текущая нагрузка всех узлов сети (для блока 'До' или 'После' на сайте)."""
    return JSONResponse(balancer.get_network_status())


class RequestsPayload(BaseModel):
    """Тело запроса для генерации входящих запросов студентов."""

    count: int = 10


@app.post("/generate_requests")
def generate_requests(body: RequestsPayload):
    """
    Смоделировать приход указанного количества запросов от студентов.

    Используется на веб‑странице: кнопка «Отправить 10 запросов».
    """
    balancer.add_requests(body.count)
    return JSONResponse(
        {
            "status": "ok",
            "generated": body.count,
            "current": balancer.get_network_status(),
        }
    )


@app.get("/balance")
def balance():
    """
    Выполнить централизованную балансировку.
    Внутри используется wave_algorithm_finn() для сбора нагрузок.
    """
    before = balancer.get_network_status()
    balancer.centralized_balancing()
    after = balancer.get_network_status()
    return JSONResponse({"before": before, "after": after})


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()

