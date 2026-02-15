# -*- coding: utf-8 -*-
import json
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.news import News
from app.database.models import NewsDB


class NewsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[News]:
        q = select(NewsDB).order_by(NewsDB.published_at.desc())
        if offset:
            q = q.offset(offset)
        if limit is not None:
            q = q.limit(limit)
        result = await self.db.execute(q)
        rows = result.scalars().all()
        return [self._to_model(r) for r in rows]

    async def get_by_id(self, news_id: str) -> Optional[News]:
        result = await self.db.execute(select(NewsDB).where(NewsDB.id == news_id))
        row = result.scalar_one_or_none()
        return self._to_model(row) if row else None

    @staticmethod
    def _to_model(row: NewsDB) -> News:
        image_urls = json.loads(row.image_urls) if isinstance(row.image_urls, str) else row.image_urls
        return News(
            id=row.id,
            message_id=row.message_id,
            title=row.title,
            text=row.text,
            image_urls=image_urls,
            media_group_id=row.media_group_id,
            published_at=row.published_at,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
