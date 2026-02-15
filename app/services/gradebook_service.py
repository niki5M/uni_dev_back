from typing import List, Optional, Dict
from app.models.grade_record import GradeRecord
from app.repositories.gradebook_repository import GradebookRepository


class GradebookService:
    def __init__(self, repository: GradebookRepository):
        self.repository = repository

    async def get_all_grades(self) -> List[GradeRecord]:
        """Получить все оценки"""
        return await self.repository.get_all_grades()

    async def get_grades_by_semester(self, semester: int) -> List[GradeRecord]:
        """Получить оценки по семестру"""
        return await self.repository.get_grades_by_semester(semester)

    async def get_grades_by_subject(self, subject: str) -> List[GradeRecord]:
        """Получить оценки по предмету"""
        return await self.repository.get_grades_by_subject(subject)

    async def get_average_grade(self) -> float:
        """Вычислить средний балл"""
        grades = await self.repository.get_all_grades()
        if not grades:
            return 0.0
        
        total = sum(grade.grade for grade in grades)
        return round(total / len(grades), 2)

    async def get_grade_statistics(self) -> Dict[str, int]:
        """Получить статистику по оценкам"""
        grades = await self.repository.get_all_grades()
        statistics: Dict[str, int] = {}
        
        for grade in grades:
            grade_str = str(grade.grade)
            statistics[grade_str] = statistics.get(grade_str, 0) + 1
        
        return statistics

