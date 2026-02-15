from sqlalchemy import Column, String, Integer, Date
from app.database.connection import Base


class GradeRecordDB(Base):
    """Модель БД для записей зачетной книжки"""
    __tablename__ = "grade_records"

    id = Column(String, primary_key=True, index=True)
    subject = Column(String, nullable=False, index=True)
    teacher = Column(String, nullable=False)
    exam_type = Column(String, nullable=False)
    grade = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False, index=True)
    date = Column(String, nullable=False)  # Храним как строку для простоты
    academic_year = Column(String, nullable=False)

    def __repr__(self):
        return f"<GradeRecordDB(id={self.id}, subject={self.subject}, grade={self.grade})>"


class ScheduleItemDB(Base):
    """Модель БД для элементов расписания. day_of_week: 1=Пн .. 7=Вс"""
    __tablename__ = "schedule_items"

    id = Column(String, primary_key=True, index=True)
    subject = Column(String, nullable=False, index=True)
    teacher = Column(String, nullable=False)
    day_of_week = Column(Integer, nullable=False, index=True)  # 1-7
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    room = Column(String, nullable=False)
    group_id = Column(String, nullable=False, index=True)
    lesson_type = Column(String, nullable=True)
    week_type = Column(String, nullable=True)  # all, odd, even

    def __repr__(self):
        return f"<ScheduleItemDB(id={self.id}, subject={self.subject}, day={self.day_of_week})>"


class NewsDB(Base):
    """Модель БД для новостей. image_urls хранится как JSON-строка."""
    __tablename__ = "news"

    id = Column(String, primary_key=True, index=True)
    message_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    image_urls = Column(String, nullable=False)  # JSON array: ["url1", "url2"]
    media_group_id = Column(String, nullable=True)
    published_at = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

    def __repr__(self):
        return f"<NewsDB(id={self.id}, title={self.title})>"



