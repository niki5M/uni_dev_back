# -*- coding: utf-8 -*-
from typing import List, Optional
from app.models.news import News
from app.repositories.news_repository import NewsRepository


class NewsService:
    def __init__(self, repository: NewsRepository):
        self.repository = repository

    async def get_all_news(self, limit: Optional[int] = None, offset: int = 0) -> List[News]:
        return await self.repository.get_all(limit=limit, offset=offset)

    async def get_news_by_id(self, news_id: str) -> Optional[News]:
        return await self.repository.get_by_id(news_id)
