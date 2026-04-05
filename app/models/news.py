# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class News(BaseModel):
    """Элемент ленты для API (совместима с NewsModel во Flutter). JSON отдаётся в camelCase."""
    model_config = ConfigDict(
        serialize_by_alias=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "1",
                "messageId": "msg_001",
                "title": "Добро пожаловать",
                "text": "Текст записи ленты...",
                "imageUrls": ["https://example.com/1.jpg"],
                "mediaGroupId": None,
                "publishedAt": "2024-09-01T10:00:00.000Z",
                "createdAt": "2024-09-01T09:00:00.000Z",
                "updatedAt": "2024-09-01T09:00:00.000Z"
            }
        }
    )
    id: str
    message_id: str = Field(..., serialization_alias="messageId", description="ID сообщения")
    title: str = Field(..., description="Заголовок")
    text: str = Field(..., description="Текст записи")
    image_urls: List[str] = Field(default_factory=list, serialization_alias="imageUrls", description="Ссылки на изображения")
    media_group_id: Optional[str] = Field(None, serialization_alias="mediaGroupId", description="ID медиагруппы")
    published_at: str = Field(..., serialization_alias="publishedAt", description="Дата публикации ISO 8601")
    created_at: str = Field(..., serialization_alias="createdAt", description="Дата создания ISO 8601")
    updated_at: str = Field(..., serialization_alias="updatedAt", description="Дата обновления ISO 8601")
