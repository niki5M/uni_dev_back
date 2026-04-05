from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.grade_record import GradeRecord, AverageGradeResponse, GradeStatisticsResponse
from app.services.gradebook_service import GradebookService
from app.repositories.gradebook_repository import GradebookRepository
from app.database.connection import get_db

router = APIRouter()


def get_gradebook_service(db: AsyncSession = Depends(get_db)) -> GradebookService:
    """Dependency для создания сервиса с репозиторием"""
    repository = GradebookRepository(db)
    return GradebookService(repository)


@router.get("/grades", response_model=List[GradeRecord])
async def get_all_grades(
    semester: Optional[int] = Query(None, description="Фильтр по номеру раздела (каталога)"),
    subject: Optional[str] = Query(None, description="Фильтр по заголовку заметки"),
    service: GradebookService = Depends(get_gradebook_service)
):
    """
    Список карточек заметок с опциональной фильтрацией по разделу или заголовку.
    """
    try:
        if semester is not None:
            return await service.get_grades_by_semester(semester)
        elif subject is not None:
            return await service.get_grades_by_subject(subject)
        else:
            return await service.get_all_grades()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching grades: {str(e)}")


@router.get("/grades/average", response_model=AverageGradeResponse)
async def get_average_grade(
    service: GradebookService = Depends(get_gradebook_service)
):
    """
    Среднее значение приоритета (поле grade) по всем карточкам.
    """
    try:
        average = await service.get_average_grade()
        return AverageGradeResponse(average=average)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating average grade: {str(e)}")


@router.get("/grades/statistics", response_model=GradeStatisticsResponse)
async def get_grade_statistics(
    service: GradebookService = Depends(get_gradebook_service)
):
    """
    Распределение карточек по значению приоритета (grade).
    """
    try:
        statistics = await service.get_grade_statistics()
        return GradeStatisticsResponse(statistics=statistics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching grade statistics: {str(e)}")

