# -*- coding: utf-8 -*-
from typing import List
from app.models.schedule_item import ScheduleItem
from app.repositories.schedule_repository import ScheduleRepository


class ScheduleService:
    def __init__(self, repository: ScheduleRepository):
        self.repository = repository

    async def get_weekly_schedule(self) -> List[ScheduleItem]:
        return await self.repository.get_all()

    async def get_daily_schedule(self, day_of_week: int) -> List[ScheduleItem]:
        return await self.repository.get_by_day(day_of_week)

    async def get_schedule_by_group(self, group_id: str) -> List[ScheduleItem]:
        return await self.repository.get_by_group(group_id)
