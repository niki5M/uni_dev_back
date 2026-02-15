from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import date


class GradeRecord(BaseModel):
    id: str
    subject: str = Field(..., description="Название предмета")
    teacher: str = Field(..., description="ФИО преподавателя")
    exam_type: str = Field(..., description="Тип экзамена: Экзамен или Зачёт")
    grade: int = Field(..., ge=2, le=5, description="Оценка от 2 до 5")
    semester: int = Field(..., ge=1, le=12, description="Номер семестра")
    date: str = Field(..., description="Дата в формате YYYY-MM-DD")
    academic_year: str = Field(..., description="Учебный год в формате YYYY-YYYY")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "subject": "Проектный практикум",
                "teacher": "Аметов Осман Мидатович",
                "exam_type": "Экзамен",
                "grade": 5,
                "semester": 1,
                "date": "2024-01-15",
                "academic_year": "2023-2024"
            }
        }


class AverageGradeResponse(BaseModel):
    average: float = Field(..., description="Средний балл")


class GradeStatisticsResponse(BaseModel):
    statistics: Dict[str, int] = Field(..., description="Статистика оценок")

