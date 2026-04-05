# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schedule_item import ScheduleItem
from app.services.schedule_service import ScheduleService
from app.repositories.schedule_repository import ScheduleRepository
from app.database.connection import get_db

router = APIRouter()


def get_schedule_service(db: AsyncSession = Depends(get_db)) -> ScheduleService:
    repository = ScheduleRepository(db)
    return ScheduleService(repository)


@router.get("/group-schedules", response_model=List[ScheduleItem])
async def get_group_schedules(
    day: Optional[int] = Query(None, description="День недели 1=Пн .. 7=Вс"),
    group: Optional[str] = Query(None, description="Идентификатор пространства (например основной)"),
    service: ScheduleService = Depends(get_schedule_service),
):
    """
    Слоты плана недели: вся неделя, один день или фильтр по пространству (group_id).
    Без параметров — полная неделя.
    """
    try:
        if day is not None:
            if day < 1 or day > 7:
                raise HTTPException(status_code=400, detail="day должен быть от 1 до 7")
            return await service.get_daily_schedule(day)
        if group is not None:
            return await service.get_schedule_by_group(group)
        return await service.get_weekly_schedule()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching schedule: {str(e)}")
