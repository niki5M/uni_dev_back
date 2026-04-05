# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.news import News
from app.services.news_service import NewsService
from app.repositories.news_repository import NewsRepository
from app.database.connection import get_db

router = APIRouter()


def get_news_service(db: AsyncSession = Depends(get_db)) -> NewsService:
    return NewsService(NewsRepository(db))


@router.get("", response_model=List[News])
async def get_news_list(
    limit: Optional[int] = Query(None, description="Максимум записей"),
    offset: int = Query(0, ge=0, description="Смещение"),
    service: NewsService = Depends(get_news_service),
):
    """Записи ленты (по дате публикации, новые первые)."""
    try:
        return await service.get_all_news(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@router.get("/{news_id}", response_model=News)
async def get_news_by_id(
    news_id: str,
    service: NewsService = Depends(get_news_service),
):
    """Элемент ленты по id."""
    news = await service.get_news_by_id(news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news
