# -*- coding: utf-8 -*-
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.schedule_item import ScheduleItem
from app.database.models import ScheduleItemDB


class ScheduleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[ScheduleItem]:
        result = await self.db.execute(select(ScheduleItemDB).order_by(ScheduleItemDB.day_of_week, ScheduleItemDB.start_time))
        rows = result.scalars().all()
        return [self._to_model(r) for r in rows]

    async def get_by_day(self, day_of_week: int) -> List[ScheduleItem]:
        result = await self.db.execute(
            select(ScheduleItemDB)
            .where(ScheduleItemDB.day_of_week == day_of_week)
            .order_by(ScheduleItemDB.start_time)
        )
        rows = result.scalars().all()
        return [self._to_model(r) for r in rows]

    async def get_by_group(self, group_id: str) -> List[ScheduleItem]:
        result = await self.db.execute(
            select(ScheduleItemDB)
            .where(ScheduleItemDB.group_id == group_id)
            .order_by(ScheduleItemDB.day_of_week, ScheduleItemDB.start_time)
        )
        rows = result.scalars().all()
        return [self._to_model(r) for r in rows]

    @staticmethod
    def _to_model(row: ScheduleItemDB) -> ScheduleItem:
        return ScheduleItem(
            id=row.id,
            subject=row.subject,
            teacher=row.teacher,
            day_of_week=row.day_of_week,
            start_time=row.start_time,
            end_time=row.end_time,
            room=row.room,
            group_id=row.group_id,
            lesson_type=row.lesson_type,
            week_type=row.week_type,
        )
