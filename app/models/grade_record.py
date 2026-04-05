from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import date


class GradeRecord(BaseModel):
    id: str
    subject: str = Field(..., description="Заголовок заметки")
    teacher: str = Field(..., description="Автор или соавтор")
    exam_type: str = Field(..., description="Статус записи, например «Черновик» или «Готово»")
    grade: int = Field(..., ge=2, le=5, description="Приоритет важности от 2 до 5")
    semester: int = Field(..., ge=1, le=12, description="Номер раздела / каталога")
    date: str = Field(..., description="Дата в формате YYYY-MM-DD")
    academic_year: str = Field(..., description="Период архива в формате YYYY-YYYY")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "subject": "Рефакторинг API",
                "teacher": "Команда бэкенда",
                "exam_type": "Готово",
                "grade": 5,
                "semester": 1,
                "date": "2024-01-15",
                "academic_year": "2023-2024"
            }
        }


class AverageGradeResponse(BaseModel):
    average: float = Field(..., description="Средний приоритет по карточкам")


class GradeStatisticsResponse(BaseModel):
    statistics: Dict[str, int] = Field(..., description="Сколько карточек на каждом уровне приоритета")

