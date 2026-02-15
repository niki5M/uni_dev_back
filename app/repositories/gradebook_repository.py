from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.grade_record import GradeRecord
from app.database.models import GradeRecordDB


class GradebookRepository:
    """Репозиторий для работы с данными зачетной книжки из БД"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_grades(self) -> List[GradeRecord]:
        """Получить все оценки"""
        result = await self.db.execute(select(GradeRecordDB))
        db_records = result.scalars().all()
        return [self._db_to_model(record) for record in db_records]

    async def get_grades_by_semester(self, semester: int) -> List[GradeRecord]:
        """Получить оценки по семестру"""
        result = await self.db.execute(
            select(GradeRecordDB).where(GradeRecordDB.semester == semester)
        )
        db_records = result.scalars().all()
        return [self._db_to_model(record) for record in db_records]

    async def get_grades_by_subject(self, subject: str) -> List[GradeRecord]:
        """Получить оценки по предмету (поиск по подстроке)"""
        result = await self.db.execute(
            select(GradeRecordDB).where(
                func.lower(GradeRecordDB.subject).contains(subject.lower())
            )
        )
        db_records = result.scalars().all()
        return [self._db_to_model(record) for record in db_records]

    @staticmethod
    def _db_to_model(db_record: GradeRecordDB) -> GradeRecord:
        """Преобразование модели БД в Pydantic модель"""
        return GradeRecord(
            id=db_record.id,
            subject=db_record.subject,
            teacher=db_record.teacher,
            exam_type=db_record.exam_type,
            grade=db_record.grade,
            semester=db_record.semester,
            date=db_record.date,
            academic_year=db_record.academic_year
        )

