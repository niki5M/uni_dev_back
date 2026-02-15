# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.v1 import gradebook, schedule, news
from app.database.connection import init_db, AsyncSessionLocal
from app.database.init_data import init_gradebook_data, init_schedule_data, init_news_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация БД при старте приложения"""
    # Инициализация БД (создание таблиц)
    await init_db()
    
    # Заполнение начальными данными
    async with AsyncSessionLocal() as db:
        await init_gradebook_data(db)
        await init_schedule_data(db)
        await init_news_data(db)
    
    yield  # Приложение работает
    
    # Здесь можно добавить код для закрытия соединений при остановке


app = FastAPI(
    title="University Backend API",
    description="Backend API for mobile university application",
    version="1.0.0",
    lifespan=lifespan,
    default_response_class=JSONResponse
)

# Настройка для корректной работы с UTF-8
@app.middleware("http")
async def add_charset_header(request, call_next):
    response = await call_next(request)
    if response.headers.get("content-type", "").startswith("application/json"):
        response.headers["content-type"] = "application/json; charset=utf-8"
    return response

# CORS middleware для работы с мобильным приложением
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(gradebook.router, prefix="/api/v1/gradebook", tags=["Gradebook"])
app.include_router(schedule.router, prefix="/api/v1/schedule", tags=["Schedule"])
# Расписание также по /api/group-schedules (для приложения с SCHEDULE_API_URL=.../api)
app.include_router(schedule.router, prefix="/api", tags=["Schedule"])
app.include_router(news.router, prefix="/api/v1/news", tags=["News"])
app.include_router(news.router, prefix="/api/news", tags=["News"])


@app.get("/")
async def root():
    return {"message": "University Backend API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

