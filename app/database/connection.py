from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Путь к базе данных SQLite с настройками кодировки UTF-8
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./university.db?charset=utf8")

# Создание асинхронного движка с настройками для UTF-8
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Установить True для отладки SQL запросов
    future=True,
    connect_args={"check_same_thread": False}  # Для SQLite
)

# Создание фабрики сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Инициализация БД: создание таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


