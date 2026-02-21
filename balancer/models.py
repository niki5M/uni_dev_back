# -*- coding: utf-8 -*-
"""Модели задач (запросов) для балансировки."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class Task(BaseModel):
    """Одна задача — имитация запроса к API (зачётка, расписание, новости)."""
    id: str = ""
    type: str = "request"  # gradebook | schedule | news
    created_at: str = ""

    def __init__(self, **data):
        if not data.get("id"):
            data["id"] = str(uuid.uuid4())[:8]
        if not data.get("created_at"):
            data["created_at"] = datetime.utcnow().isoformat() + "Z"
        super().__init__(**data)
