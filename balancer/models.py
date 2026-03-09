"""
Модели для очередей задач воркеров.
"""
from pydantic import BaseModel


class Task(BaseModel):
    """Задача студента: тип запроса (зачётка, расписание, новости)."""
    type: str = "gradebook"  # gradebook | schedule | news
