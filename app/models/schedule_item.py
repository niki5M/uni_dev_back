# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional


class ScheduleItem(BaseModel):
    """Элемент расписания для API (совместим с ScheduleItemModel во Flutter)"""
    id: str
    subject: str = Field(..., description="Название предмета")
    teacher: str = Field(..., description="ФИО преподавателя")
    day_of_week: int = Field(..., ge=1, le=7, description="День недели 1=Пн .. 7=Вс")
    start_time: str = Field(..., description="Начало пары, например 08:00")
    end_time: str = Field(..., description="Конец пары, например 09:30")
    room: str = Field(..., description="Аудитория")
    group_id: str = Field(..., description="Идентификатор группы")
    lesson_type: Optional[str] = Field(None, description="Тип: лекция, практика, лаб. работа")
    week_type: Optional[str] = Field(None, description="Тип недели: all, odd, even")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "subject": "ООП",
                "teacher": "Сейдаметов Гирей Серверович",
                "day_of_week": 1,
                "start_time": "08:00",
                "end_time": "09:30",
                "room": "ауд. 301",
                "group_id": "ИС-41",
                "lesson_type": "Лекция",
                "week_type": "all"
            }
        }
