"""
Модели для очередей задач воркеров.
"""
from pydantic import BaseModel


class Task(BaseModel):
    """Демо-задача к API заметок: gradebook, schedule или news."""
    type: str = "gradebook"  # gradebook | schedule | news
