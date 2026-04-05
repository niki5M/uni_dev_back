# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional


class ScheduleItem(BaseModel):
    """Слот плана недели для API (совместим с ScheduleItemModel во Flutter)"""
    id: str
    subject: str = Field(..., description="Название блока или темы заметки")
    teacher: str = Field(..., description="Ответственный или участник")
    day_of_week: int = Field(..., ge=1, le=7, description="День недели 1=Пн .. 7=Вс")
    start_time: str = Field(..., description="Начало слота, например 08:00")
    end_time: str = Field(..., description="Конец слота, например 09:30")
    room: str = Field(..., description="Место: офис, дом, кафе и т.д.")
    group_id: str = Field(..., description="Пространство / доска (идентификатор)")
    lesson_type: Optional[str] = Field(None, description="Режим: фокус, обзор, синк")
    week_type: Optional[str] = Field(None, description="Тип недели: all, odd, even")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "subject": "Глубокая работа: дизайн",
                "teacher": "Я",
                "day_of_week": 1,
                "start_time": "08:00",
                "end_time": "09:30",
                "room": "дом, кабинет",
                "group_id": "основной",
                "lesson_type": "Фокус",
                "week_type": "all"
            }
        }
