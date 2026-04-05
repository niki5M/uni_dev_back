# -*- coding: utf-8 -*-
"""
Инициализация БД демо-данными сервиса заметок.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
from app.database.models import GradeRecordDB, ScheduleItemDB, NewsDB


async def init_gradebook_data(db: AsyncSession):
    """Заполнение БД карточками заметок (метаданные в тех же полях, что и раньше)."""
    
    # Проверяем, есть ли уже данные
    result = await db.execute(select(GradeRecordDB))
    existing_records = result.scalars().all()
    
    if existing_records:
        print("Данные уже существуют в БД, пропускаем инициализацию")
        return
    
    # Начальные данные (40 карточек заметок)
    initial_data = [
        {
            "id": "1",
            "subject": "Идеи для спринта",
            "teacher": "Аня К.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 1,
            "date": "2024-01-15",
            "academic_year": "2023-2024",
        },
        {
            "id": "2",
            "subject": "Чек-лист релиза",
            "teacher": "Сергей Л.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 1,
            "date": "2024-01-20",
            "academic_year": "2023-2024",
        },
        {
            "id": "3",
            "subject": "Структура документации",
            "teacher": "Марина П.",
            "exam_type": "Черновик",
            "grade": 3,
            "semester": 1,
            "date": "2024-01-25",
            "academic_year": "2023-2024",
        },
        {
            "id": "4",
            "subject": "Схема БД заметок",
            "teacher": "Илья В.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 1,
            "date": "2024-01-30",
            "academic_year": "2023-2024",
        },
        {
            "id": "5",
            "subject": "Алгоритм синхронизации",
            "teacher": "Олег Т.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 1,
            "date": "2024-02-05",
            "academic_year": "2023-2024",
        },
        {
            "id": "6",
            "subject": "Теги и фильтры",
            "teacher": "Катя С.",
            "exam_type": "Черновик",
            "grade": 4,
            "semester": 1,
            "date": "2024-02-10",
            "academic_year": "2023-2024",
        },
        {
            "id": "7",
            "subject": "Шаблон ежедневника",
            "teacher": "Дима Н.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 1,
            "date": "2024-02-12",
            "academic_year": "2023-2024",
        },
        {
            "id": "8",
            "subject": "Цитаты для статьи",
            "teacher": "Лена Р.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 1,
            "date": "2024-02-15",
            "academic_year": "2023-2024",
        },
        {
            "id": "9",
            "subject": "Ретро команды",
            "teacher": "Павел Ю.",
            "exam_type": "Черновик",
            "grade": 3,
            "semester": 1,
            "date": "2024-02-18",
            "academic_year": "2023-2024",
        },
        {
            "id": "10",
            "subject": "Формулировка ТЗ",
            "teacher": "Настя М.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 1,
            "date": "2024-02-20",
            "academic_year": "2023-2024",
        },
        {
            "id": "11",
            "subject": "Мокапы экрана списка",
            "teacher": "Артём Ф.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 1,
            "date": "2024-02-22",
            "academic_year": "2023-2024",
        },
        {
            "id": "12",
            "subject": "Скрипт миграции",
            "teacher": "Юля Г.",
            "exam_type": "Черновик",
            "grade": 5,
            "semester": 1,
            "date": "2024-02-25",
            "academic_year": "2023-2024",
        },
        {
            "id": "13",
            "subject": "Архив скриншотов",
            "teacher": "Миша Д.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 1,
            "date": "2024-02-28",
            "academic_year": "2023-2024",
        },
        {
            "id": "14",
            "subject": "Бюджет на подписки",
            "teacher": "Оля З.",
            "exam_type": "Готово",
            "grade": 3,
            "semester": 1,
            "date": "2024-03-01",
            "academic_year": "2023-2024",
        },
        {
            "id": "15",
            "subject": "Метрики удержания",
            "teacher": "Вика Е.",
            "exam_type": "Черновик",
            "grade": 4,
            "semester": 1,
            "date": "2024-03-05",
            "academic_year": "2023-2024",
        },
        {
            "id": "16",
            "subject": "Политика приватности",
            "teacher": "Роман Б.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 1,
            "date": "2024-03-08",
            "academic_year": "2023-2024",
        },
        {
            "id": "17",
            "subject": "Подбор шрифтов",
            "teacher": "Света Ж.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 1,
            "date": "2024-03-10",
            "academic_year": "2023-2024",
        },
        {
            "id": "18",
            "subject": "Интеграция календаря",
            "teacher": "Гоша Х.",
            "exam_type": "Черновик",
            "grade": 3,
            "semester": 1,
            "date": "2024-03-12",
            "academic_year": "2023-2024",
        },
        {
            "id": "19",
            "subject": "User stories v2",
            "teacher": "Тимур Ц.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 1,
            "date": "2024-03-15",
            "academic_year": "2023-2024",
        },
        {
            "id": "20",
            "subject": "План на квартал",
            "teacher": "Вова Щ.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 1,
            "date": "2024-03-18",
            "academic_year": "2023-2024",
        },
        {
            "id": "21",
            "subject": "Рефакторинг поиска",
            "teacher": "Аня К.",
            "exam_type": "Черновик",
            "grade": 3,
            "semester": 2,
            "date": "2024-06-10",
            "academic_year": "2023-2024",
        },
        {
            "id": "22",
            "subject": "Долг: старый импорт",
            "teacher": "Сергей Л.",
            "exam_type": "Готово",
            "grade": 2,
            "semester": 2,
            "date": "2024-06-15",
            "academic_year": "2023-2024",
        },
        {
            "id": "23",
            "subject": "Черновик онбординга",
            "teacher": "Марина П.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 2,
            "date": "2024-06-20",
            "academic_year": "2023-2024",
        },
        {
            "id": "24",
            "subject": "Push-напоминания",
            "teacher": "Илья В.",
            "exam_type": "Черновик",
            "grade": 5,
            "semester": 2,
            "date": "2024-06-22",
            "academic_year": "2023-2024",
        },
        {
            "id": "25",
            "subject": "Экспорт в Markdown",
            "teacher": "Олег Т.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 2,
            "date": "2024-06-25",
            "academic_year": "2023-2024",
        },
        {
            "id": "26",
            "subject": "Шифрование локально",
            "teacher": "Катя С.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 2,
            "date": "2024-06-28",
            "academic_year": "2023-2024",
        },
        {
            "id": "27",
            "subject": "Виджет быстрой записи",
            "teacher": "Дима Н.",
            "exam_type": "Черновик",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-01",
            "academic_year": "2023-2024",
        },
        {
            "id": "28",
            "subject": "Голосовые заметки",
            "teacher": "Лена Р.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 2,
            "date": "2024-07-03",
            "academic_year": "2023-2024",
        },
        {
            "id": "29",
            "subject": "Версионирование карточек",
            "teacher": "Павел Ю.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 2,
            "date": "2024-07-05",
            "academic_year": "2023-2024",
        },
        {
            "id": "30",
            "subject": "Тест-кейсы UI",
            "teacher": "Настя М.",
            "exam_type": "Черновик",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-08",
            "academic_year": "2023-2024",
        },
        {
            "id": "31",
            "subject": "Гайд по стилю UI",
            "teacher": "Артём Ф.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 2,
            "date": "2024-07-10",
            "academic_year": "2023-2024",
        },
        {
            "id": "32",
            "subject": "Очередь фоновой синхронизации",
            "teacher": "Юля Г.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-12",
            "academic_year": "2023-2024",
        },
        {
            "id": "33",
            "subject": "Локализация EN",
            "teacher": "Миша Д.",
            "exam_type": "Черновик",
            "grade": 3,
            "semester": 2,
            "date": "2024-07-15",
            "academic_year": "2023-2024",
        },
        {
            "id": "34",
            "subject": "Аналитика событий",
            "teacher": "Оля З.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-18",
            "academic_year": "2023-2024",
        },
        {
            "id": "35",
            "subject": "Облачный бэкап",
            "teacher": "Вика Е.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 2,
            "date": "2024-07-20",
            "academic_year": "2023-2024",
        },
        {
            "id": "36",
            "subject": "Оптимизация списков",
            "teacher": "Роман Б.",
            "exam_type": "Черновик",
            "grade": 3,
            "semester": 2,
            "date": "2024-07-22",
            "academic_year": "2023-2024",
        },
        {
            "id": "37",
            "subject": "Обложки блокнотов",
            "teacher": "Света Ж.",
            "exam_type": "Готово",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-25",
            "academic_year": "2023-2024",
        },
        {
            "id": "38",
            "subject": "Подсказки ИИ",
            "teacher": "Гоша Х.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 2,
            "date": "2024-07-28",
            "academic_year": "2023-2024",
        },
        {
            "id": "39",
            "subject": "Roadmap продукта",
            "teacher": "Тимур Ц.",
            "exam_type": "Черновик",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-30",
            "academic_year": "2023-2024",
        },
        {
            "id": "40",
            "subject": "Шаблон встречи 1:1",
            "teacher": "Вова Щ.",
            "exam_type": "Готово",
            "grade": 5,
            "semester": 2,
            "date": "2024-08-02",
            "academic_year": "2023-2024",
        },
    ]
    
    # Создаем записи в БД
    for data in initial_data:
        grade_record = GradeRecordDB(**data)
        db.add(grade_record)
    
    await db.commit()
    print(f"Инициализировано {len(initial_data)} записей в БД (карточки заметок)")


async def init_schedule_data(db: AsyncSession):
    """Заполнение БД слотами плана недели (~50 записей). day_of_week: 1=Пн .. 7=Вс"""
    result = await db.execute(select(ScheduleItemDB))
    existing = result.scalars().all()
    if existing:
        print("Данные плана недели уже есть в БД, пропускаем инициализацию")
        return

    initial_data = [
        {"id": "s1", "subject": "Утренний обзор задач", "teacher": "Я", "day_of_week": 1, "start_time": "08:00", "end_time": "09:30", "room": "дом, стол", "group_id": "основной", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s2", "subject": "Планирование недели", "teacher": "Команда", "day_of_week": 1, "start_time": "09:45", "end_time": "11:15", "room": "коворкинг А", "group_id": "основной", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s3", "subject": "Глубокая работа: API", "teacher": "Настя", "day_of_week": 1, "start_time": "11:30", "end_time": "13:00", "room": "дом, кабинет", "group_id": "основной", "lesson_type": "Фокус", "week_type": "odd"},
        {"id": "s4", "subject": "Синк с дизайном", "teacher": "Продакт", "day_of_week": 1, "start_time": "13:50", "end_time": "15:20", "room": "Zoom", "group_id": "команда", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s5", "subject": "Ревью pull request", "teacher": "Ты", "day_of_week": 1, "start_time": "15:35", "end_time": "17:05", "room": "офис, переговорка", "group_id": "команда", "lesson_type": "Фокус", "week_type": "even"},
        {"id": "s6", "subject": "Разбор бэклога", "teacher": "Я", "day_of_week": 2, "start_time": "08:00", "end_time": "09:30", "room": "дом, кухня", "group_id": "основной", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s7", "subject": "Воркшоп по тегам", "teacher": "Команда", "day_of_week": 2, "start_time": "09:45", "end_time": "11:15", "room": "офис, open space", "group_id": "основной", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s8", "subject": "Структура папок", "teacher": "Настя", "day_of_week": 2, "start_time": "11:30", "end_time": "13:00", "room": "дом, диван", "group_id": "основной", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s9", "subject": "Прототип поиска", "teacher": "Продакт", "day_of_week": 2, "start_time": "13:50", "end_time": "15:20", "room": "кафе у дома", "group_id": "личное", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s10", "subject": "Настройка CI", "teacher": "Ты", "day_of_week": 2, "start_time": "15:35", "end_time": "17:05", "room": "дом, балкон", "group_id": "личное", "lesson_type": "Синк", "week_type": "odd"},
        {"id": "s11", "subject": "Инбокс нулевой", "teacher": "Я", "day_of_week": 3, "start_time": "08:00", "end_time": "09:30", "room": "парк", "group_id": "основной", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s12", "subject": "Карта контента", "teacher": "Команда", "day_of_week": 3, "start_time": "09:45", "end_time": "11:15", "room": "спортзал", "group_id": "основной", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s13", "subject": "Шаблоны заметок", "teacher": "Настя", "day_of_week": 3, "start_time": "11:30", "end_time": "13:00", "room": "дом", "group_id": "основной", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s14", "subject": "Демо для стейкхолдеров", "teacher": "Продакт", "day_of_week": 3, "start_time": "13:50", "end_time": "15:20", "room": "онлайн", "group_id": "команда", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s15", "subject": "Вечерний дауншифт", "teacher": "Ты", "day_of_week": 3, "start_time": "15:35", "end_time": "17:05", "room": "дом, спальня", "group_id": "команда", "lesson_type": "Фокус", "week_type": "even"},
        {"id": "s16", "subject": "Прогулка + диктовка", "teacher": "Я", "day_of_week": 4, "start_time": "08:00", "end_time": "09:30", "room": "дом, стол", "group_id": "основной", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s17", "subject": "Подготовка к ретро", "teacher": "Команда", "day_of_week": 4, "start_time": "09:45", "end_time": "11:15", "room": "коворкинг А", "group_id": "основной", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s18", "subject": "Викенд-чтение", "teacher": "Настя", "day_of_week": 4, "start_time": "11:30", "end_time": "13:00", "room": "дом, кабинет", "group_id": "команда", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s19", "subject": "Личный дневник", "teacher": "Продакт", "day_of_week": 4, "start_time": "13:50", "end_time": "15:20", "room": "Zoom", "group_id": "команда", "lesson_type": "Обзор", "week_type": "odd"},
        {"id": "s20", "subject": "Быстрые мысли", "teacher": "Ты", "day_of_week": 4, "start_time": "15:35", "end_time": "17:05", "room": "офис, переговорка", "group_id": "личное", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s21", "subject": "Семейный календарь", "teacher": "Я", "day_of_week": 5, "start_time": "08:00", "end_time": "09:30", "room": "дом, кухня", "group_id": "основной", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s22", "subject": "Покупки и списки", "teacher": "Команда", "day_of_week": 5, "start_time": "09:45", "end_time": "11:15", "room": "офис, open space", "group_id": "основной", "lesson_type": "Синк", "week_type": "even"},
        {"id": "s23", "subject": "Идеи для блога", "teacher": "Настя", "day_of_week": 5, "start_time": "11:30", "end_time": "13:00", "room": "дом, диван", "group_id": "основной", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s24", "subject": "Медитация 10 мин", "teacher": "Продакт", "day_of_week": 5, "start_time": "13:50", "end_time": "15:20", "room": "кафе у дома", "group_id": "команда", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s25", "subject": "План тренировки", "teacher": "Ты", "day_of_week": 5, "start_time": "15:35", "end_time": "17:05", "room": "дом, балкон", "group_id": "команда", "lesson_type": "Фокус", "week_type": "odd"},
        {"id": "s26", "subject": "Учебные конспекты", "teacher": "Я", "day_of_week": 5, "start_time": "17:20", "end_time": "18:50", "room": "парк", "group_id": "личное", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s27", "subject": "Рецепты на неделю", "teacher": "Команда", "day_of_week": 1, "start_time": "08:00", "end_time": "09:30", "room": "спортзал", "group_id": "личное", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s28", "subject": "Фокус: мобильный UI", "teacher": "Настя", "day_of_week": 1, "start_time": "09:45", "end_time": "11:15", "room": "дом", "group_id": "личное", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s29", "subject": "Напоминания по проекту", "teacher": "Продакт", "day_of_week": 2, "start_time": "08:00", "end_time": "09:30", "room": "онлайн", "group_id": "личное", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s30", "subject": "Финансовый учёт", "teacher": "Ты", "day_of_week": 2, "start_time": "11:30", "end_time": "13:00", "room": "дом, спальня", "group_id": "личное", "lesson_type": "Синк", "week_type": "even"},
        {"id": "s31", "subject": "Чтение RSS", "teacher": "Я", "day_of_week": 3, "start_time": "13:50", "end_time": "15:20", "room": "дом, стол", "group_id": "личное", "lesson_type": "Обзор", "week_type": "odd"},
        {"id": "s32", "subject": "Парольный менеджер", "teacher": "Команда", "day_of_week": 4, "start_time": "08:00", "end_time": "09:30", "room": "коворкинг А", "group_id": "личное", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s33", "subject": "Цели на месяц", "teacher": "Настя", "day_of_week": 4, "start_time": "11:30", "end_time": "13:00", "room": "дом, кабинет", "group_id": "личное", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s34", "subject": "Встреча с ментором", "teacher": "Продакт", "day_of_week": 5, "start_time": "08:00", "end_time": "09:30", "room": "Zoom", "group_id": "личное", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s35", "subject": "Код-ревью архив", "teacher": "Ты", "day_of_week": 6, "start_time": "09:45", "end_time": "11:15", "room": "офис, переговорка", "group_id": "основной", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s36", "subject": "Очистка тегов", "teacher": "Я", "day_of_week": 6, "start_time": "11:30", "end_time": "13:00", "room": "дом, кухня", "group_id": "основной", "lesson_type": "Фокус", "week_type": "odd"},
        {"id": "s37", "subject": "Экспорт в PDF", "teacher": "Команда", "day_of_week": 6, "start_time": "13:50", "end_time": "15:20", "room": "офис, open space", "group_id": "команда", "lesson_type": "Обзор", "week_type": "even"},
        {"id": "s38", "subject": "Бэкап в облако", "teacher": "Настя", "day_of_week": 6, "start_time": "15:35", "end_time": "17:05", "room": "дом, диван", "group_id": "команда", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s39", "subject": "Шаринг с командой", "teacher": "Продакт", "day_of_week": 6, "start_time": "08:00", "end_time": "09:30", "room": "кафе у дома", "group_id": "личное", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s40", "subject": "План спринта", "teacher": "Ты", "day_of_week": 6, "start_time": "09:45", "end_time": "11:15", "room": "дом, балкон", "group_id": "личное", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s41", "subject": "Глубокое чтение", "teacher": "Я", "day_of_week": 2, "start_time": "13:50", "end_time": "15:20", "room": "парк", "group_id": "команда", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s42", "subject": "Вечер без экрана", "teacher": "Команда", "day_of_week": 3, "start_time": "08:00", "end_time": "09:30", "room": "спортзал", "group_id": "команда", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s43", "subject": "Подкасты и цитаты", "teacher": "Настя", "day_of_week": 4, "start_time": "11:30", "end_time": "13:00", "room": "дом", "group_id": "основной", "lesson_type": "Фокус", "week_type": "even"},
        {"id": "s44", "subject": "Субботний обзор", "teacher": "Продакт", "day_of_week": 5, "start_time": "11:30", "end_time": "13:00", "room": "онлайн", "group_id": "личное", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s45", "subject": "Воскресный план", "teacher": "Ты", "day_of_week": 1, "start_time": "13:50", "end_time": "15:20", "room": "дом, спальня", "group_id": "личное", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s46", "subject": "Повторение интервью", "teacher": "Я", "day_of_week": 2, "start_time": "15:35", "end_time": "17:05", "room": "дом, стол", "group_id": "команда", "lesson_type": "Обзор", "week_type": "all"},
        {"id": "s47", "subject": "Карьерные цели", "teacher": "Команда", "day_of_week": 3, "start_time": "15:35", "end_time": "17:05", "room": "коворкинг А", "group_id": "команда", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s48", "subject": "Проект «дом»", "teacher": "Настя", "day_of_week": 4, "start_time": "15:35", "end_time": "17:05", "room": "дом, кабинет", "group_id": "основной", "lesson_type": "Фокус", "week_type": "odd"},
        {"id": "s49", "subject": "Встреча 1:1", "teacher": "Продакт", "day_of_week": 5, "start_time": "08:00", "end_time": "09:30", "room": "Zoom", "group_id": "команда", "lesson_type": "Фокус", "week_type": "all"},
        {"id": "s50", "subject": "Личные напоминания", "teacher": "Ты", "day_of_week": 6, "start_time": "15:35", "end_time": "17:05", "room": "офис, переговорка", "group_id": "личное", "lesson_type": "Фокус", "week_type": "all"},
    ]

    for data in initial_data:
        db.add(ScheduleItemDB(**data))
    await db.commit()
    print(f"Инициализировано {len(initial_data)} записей в БД (план недели)")


async def init_news_data(db: AsyncSession):
    """Заполнение БД записями ленты."""
    result = await db.execute(select(NewsDB))
    if result.scalars().first():
        print("Данные ленты уже есть в БД, пропускаем инициализацию")
        return

    def dt(s: str) -> str:
        return s  # ISO 8601 строки как есть

    initial_data = [
        {"id": "n1", "message_id": "msg_001", "title": "Добро пожаловать в Notes", "text": "Здесь карточки с приоритетом, план недели и лента обновлений. Сохраняйте идеи, блоки времени и материалы в одном месте.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-01T10:00:00.000Z"), "created_at": dt("2024-09-01T09:00:00.000Z"), "updated_at": dt("2024-09-01T09:00:00.000Z")},
        {"id": "n2", "message_id": "msg_002", "title": "Новый сезон записей", "text": "С 2 сентября включены напоминания по плану недели. Проверьте слоты в разделе плана и при необходимости перенесите время.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-08-28T12:00:00.000Z"), "created_at": dt("2024-08-28T11:00:00.000Z"), "updated_at": dt("2024-08-28T11:00:00.000Z")},
        {"id": "n3", "message_id": "msg_003", "title": "Шаблоны для быстрого старта", "text": "До 15 сентября в галерее доступны новые шаблоны: дневник, проект, встреча. Выберите в настройках блокнота.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-04T08:00:00.000Z"), "created_at": dt("2024-09-04T07:30:00.000Z"), "updated_at": dt("2024-09-04T07:30:00.000Z")},
        {"id": "n4", "message_id": "msg_004", "title": "Совместные блокноты", "text": "Приглашайте соавторов в пространство «команда»: общие теги, комментарии и история правок.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-08T14:00:00.000Z"), "created_at": dt("2024-09-08T13:00:00.000Z"), "updated_at": dt("2024-09-08T13:00:00.000Z")},
        {"id": "n5", "message_id": "msg_005", "title": "Марафон идей в октябре", "text": "Целый месяц — челлендж: одна короткая заметка в день. Итоги и призы — в ленте 1 ноября.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-15T09:00:00.000Z"), "created_at": dt("2024-09-15T08:00:00.000Z"), "updated_at": dt("2024-09-15T08:00:00.000Z")},
        {"id": "n6", "message_id": "msg_006", "title": "Изменение плана на 20 сентября", "text": "В понедельник блок «Глубокая работа: API» для пространства «основной» сдвинут с 11:30 на 15:35. Место без изменений.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-18T16:00:00.000Z"), "created_at": dt("2024-09-18T15:00:00.000Z"), "updated_at": dt("2024-09-18T15:00:00.000Z")},
        {"id": "n7", "message_id": "msg_007", "title": "Подборка статей в ленте", "text": "Мы добавили в ленту подборку про продуктивность и удержание фокуса. Сохраняйте понравившиеся ссылки в заметку одним тапом.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-20T11:00:00.000Z"), "created_at": dt("2024-09-20T10:00:00.000Z"), "updated_at": dt("2024-09-20T10:00:00.000Z")},
        {"id": "n8", "message_id": "msg_008", "title": "Интеграция с календарём", "text": "Подключите календарь: слоты плана недели можно экспортировать как события. Настройки — в профиле.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-21T08:00:00.000Z"), "created_at": dt("2024-09-21T07:00:00.000Z"), "updated_at": dt("2024-09-21T07:00:00.000Z")},
        {"id": "n9", "message_id": "msg_009", "title": "Вебинар: порядок в заметках", "text": "25 сентября в 15:00 — открытый вебинар о системе тегов и поиске. Ссылка придёт в рассылке, регистрация обязательна.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-22T12:00:00.000Z"), "created_at": dt("2024-09-22T11:00:00.000Z"), "updated_at": dt("2024-09-22T11:00:00.000Z")},
        {"id": "n10", "message_id": "msg_010", "title": "Неделя чистого инбокса", "text": "С 1 по 7 октября предлагаем пройти челлендж «ноль необработанных». Подсказки ежедневно в ленте.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-25T10:00:00.000Z"), "created_at": dt("2024-09-25T09:00:00.000Z"), "updated_at": dt("2024-09-25T09:00:00.000Z")},
        {"id": "n11", "message_id": "msg_011", "title": "Технические работы", "text": "28 сентября с 02:00 до 06:00 возможны перебои синхронизации. Локальные заметки останутся доступны офлайн.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-26T14:00:00.000Z"), "created_at": dt("2024-09-26T13:00:00.000Z"), "updated_at": dt("2024-09-26T13:00:00.000Z")},
        {"id": "n12", "message_id": "msg_012", "title": "Подписка Plus: продление", "text": "Активные подписчики Plus получают скидку 20% при продлении до 10 октября. Условия в разделе «Подписка».", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-27T09:00:00.000Z"), "created_at": dt("2024-09-27T08:00:00.000Z"), "updated_at": dt("2024-09-27T08:00:00.000Z")},
        {"id": "n13", "message_id": "msg_013", "title": "Чек-лист перед релизом", "text": "Мы опубликовали готовый чек-лист для финальной проверки фич. Скопируйте в свой блокнот и отмечайте пункты.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-10-01T11:00:00.000Z"), "created_at": dt("2024-10-01T10:00:00.000Z"), "updated_at": dt("2024-10-01T10:00:00.000Z")},
        {"id": "n14", "message_id": "msg_014", "title": "День открытых шаблонов", "text": "12 октября — витрина шаблонов от сообщества. Голосуйте за понравившиеся — победители попадут в приложение.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-10-03T15:00:00.000Z"), "created_at": dt("2024-10-03T14:00:00.000Z"), "updated_at": dt("2024-10-03T14:00:00.000Z")},
        {"id": "n15", "message_id": "msg_015", "title": "Обновление приложения", "text": "Новая версия: пуши по слотам плана и превью вложений в ленте. Обновитесь в магазине приложений.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-10-05T12:00:00.000Z"), "created_at": dt("2024-10-05T11:00:00.000Z"), "updated_at": dt("2024-10-05T11:00:00.000Z")},
    ]

    for data in initial_data:
        db.add(NewsDB(**data))
    await db.commit()
    print(f"Инициализировано {len(initial_data)} записей в БД (лента)")


