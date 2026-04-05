# -*- coding: utf-8 -*-
"""
Веб-сервер для лабораторной 7–10:
- /status  — текущая нагрузка узлов;
- /balance — шаг централизованной балансировки (волновой алгоритм Финна);
- /generate_requests — смоделировать поступление задач.

Демо-роутер подключается к app.main (порт 8000); отдельный запуск — python -m balancer.server_finn.
"""

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from balancer.network import NetworkBalancer

router = APIRouter(tags=["Finn demo"])
balancer = NetworkBalancer()


@router.get("/status")
def get_status():
    """Текущая нагрузка узлов (для таблиц «до / после» на index.html)."""
    return JSONResponse(balancer.get_network_status())


class RequestsPayload(BaseModel):
    """Тело запроса: сколько задач добавить в симуляцию."""

    count: int = 10


@router.post("/generate_requests")
def generate_requests(body: RequestsPayload):
    """Смоделировать поступление задач во входной узел (перекос перед балансировкой)."""
    balancer.add_requests(body.count)
    return JSONResponse(
        {
            "status": "ok",
            "generated": body.count,
            "current": balancer.get_network_status(),
        }
    )


@router.get("/balance")
def balance():
    """Централизованная балансировка нагрузки по узлам."""
    before = balancer.get_network_status()
    balancer.centralized_balancing()
    after = balancer.get_network_status()
    return JSONResponse({"before": before, "after": after})


def create_app() -> FastAPI:
    application = FastAPI(title="Finn Network Balancer")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(router)
    return application


app = create_app()


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
