# -*- coding: utf-8 -*-
"""
Скрипт для инициализации БД с начальными данными
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
from app.database.models import GradeRecordDB, ScheduleItemDB, NewsDB


async def init_gradebook_data(db: AsyncSession):
    """Заполнение БД начальными данными зачетной книжки"""
    
    # Проверяем, есть ли уже данные
    result = await db.execute(select(GradeRecordDB))
    existing_records = result.scalars().all()
    
    if existing_records:
        print("Данные уже существуют в БД, пропускаем инициализацию")
        return
    
    # Начальные данные (40 записей)
    initial_data = [
        # Семестр 1, 2023-2024
        {
            "id": "1",
            "subject": "Проектный практикум",
            "teacher": "Аметов Осман Мидатович",
            "exam_type": "Экзамен",
            "grade": 5,
            "semester": 1,
            "date": "2024-01-15",
            "academic_year": "2023-2024",
        },
        {
            "id": "2",
            "subject": "ООП",
            "teacher": "Сейдаметов Гирей Серверович",
            "exam_type": "Зачёт",
            "grade": 4,
            "semester": 1,
            "date": "2024-01-20",
            "academic_year": "2023-2024",
        },
        {
            "id": "3",
            "subject": "Математическая логика",
            "teacher": "Абдураманов Зиннур Шевкетович",
            "exam_type": "Экзамен",
            "grade": 3,
            "semester": 1,
            "date": "2024-01-25",
            "academic_year": "2023-2024",
        },
        {
            "id": "4",
            "subject": "Базы данных",
            "teacher": "Иванов Иван Иванович",
            "exam_type": "Экзамен",
            "grade": 5,
            "semester": 1,
            "date": "2024-01-30",
            "academic_year": "2023-2024",
        },
        {
            "id": "5",
            "subject": "Алгоритмы и структуры данных",
            "teacher": "Сидоров Сидор Сидорович",
            "exam_type": "Экзамен",
            "grade": 5,
            "semester": 1,
            "date": "2024-02-05",
            "academic_year": "2023-2024",
        },
        {
            "id": "6",
            "subject": "Дискретная математика",
            "teacher": "Козлова Мария Петровна",
            "exam_type": "Экзамен",
            "grade": 4,
            "semester": 1,
            "date": "2024-02-10",
            "academic_year": "2023-2024",
        },
        {
            "id": "7",
            "subject": "Информатика",
            "teacher": "Новиков Алексей Владимирович",
            "exam_type": "Зачёт",
            "grade": 5,
            "semester": 1,
            "date": "2024-02-12",
            "academic_year": "2023-2024",
        },
        {
            "id": "8",
            "subject": "Иностранный язык",
            "teacher": "Смирнова Елена Александровна",
            "exam_type": "Зачёт",
            "grade": 4,
            "semester": 1,
            "date": "2024-02-15",
            "academic_year": "2023-2024",
        },
        {
            "id": "9",
            "subject": "Физика",
            "teacher": "Волков Дмитрий Сергеевич",
            "exam_type": "Экзамен",
            "grade": 3,
            "semester": 1,
            "date": "2024-02-18",
            "academic_year": "2023-2024",
        },
        {
            "id": "10",
            "subject": "История",
            "teacher": "Петрова Анна Игоревна",
            "exam_type": "Зачёт",
            "grade": 4,
            "semester": 1,
            "date": "2024-02-20",
            "academic_year": "2023-2024",
        },
        {
            "id": "11",
            "subject": "Линейная алгебра",
            "teacher": "Морозов Сергей Николаевич",
            "exam_type": "Экзамен",
            "grade": 4,
            "semester": 1,
            "date": "2024-02-22",
            "academic_year": "2023-2024",
        },
        {
            "id": "12",
            "subject": "Программирование на Python",
            "teacher": "Лебедев Андрей Викторович",
            "exam_type": "Зачёт",
            "grade": 5,
            "semester": 1,
            "date": "2024-02-25",
            "academic_year": "2023-2024",
        },
        {
            "id": "13",
            "subject": "Архитектура компьютеров",
            "teacher": "Федоров Игорь Борисович",
            "exam_type": "Экзамен",
            "grade": 4,
            "semester": 1,
            "date": "2024-02-28",
            "academic_year": "2023-2024",
        },
        {
            "id": "14",
            "subject": "Экономика",
            "teacher": "Кузнецова Ольга Дмитриевна",
            "exam_type": "Зачёт",
            "grade": 3,
            "semester": 1,
            "date": "2024-03-01",
            "academic_year": "2023-2024",
        },
        {
            "id": "15",
            "subject": "Теория вероятностей",
            "teacher": "Орлов Павел Алексеевич",
            "exam_type": "Экзамен",
            "grade": 4,
            "semester": 1,
            "date": "2024-03-05",
            "academic_year": "2023-2024",
        },
        {
            "id": "16",
            "subject": "Операционные системы",
            "teacher": "Романов Виктор Иванович",
            "exam_type": "Экзамен",
            "grade": 5,
            "semester": 1,
            "date": "2024-03-08",
            "academic_year": "2023-2024",
        },
        {
            "id": "17",
            "subject": "Компьютерная графика",
            "teacher": "Соколова Наталья Сергеевна",
            "exam_type": "Зачёт",
            "grade": 4,
            "semester": 1,
            "date": "2024-03-10",
            "academic_year": "2023-2024",
        },
        {
            "id": "18",
            "subject": "Сетевые технологии",
            "teacher": "Белов Максим Андреевич",
            "exam_type": "Экзамен",
            "grade": 3,
            "semester": 1,
            "date": "2024-03-12",
            "academic_year": "2023-2024",
        },
        {
            "id": "19",
            "subject": "Математический анализ",
            "teacher": "Григорьев Александр Петрович",
            "exam_type": "Экзамен",
            "grade": 4,
            "semester": 1,
            "date": "2024-03-15",
            "academic_year": "2023-2024",
        },
        {
            "id": "20",
            "subject": "Физкультура",
            "teacher": "Ткачев Иван Сергеевич",
            "exam_type": "Зачёт",
            "grade": 5,
            "semester": 1,
            "date": "2024-03-18",
            "academic_year": "2023-2024",
        },
        # Семестр 2, 2023-2024
        {
            "id": "21",
            "subject": "Математическая логика",
            "teacher": "Абдураманов Зиннур Шевкетович",
            "exam_type": "Экзамен",
            "grade": 3,
            "semester": 2,
            "date": "2024-06-10",
            "academic_year": "2023-2024",
        },
        {
            "id": "22",
            "subject": "Системное программирование",
            "teacher": "Абдураманов Зиннур Шевкетович",
            "exam_type": "Экзамен",
            "grade": 2,
            "semester": 2,
            "date": "2024-06-15",
            "academic_year": "2023-2024",
        },
        {
            "id": "23",
            "subject": "Веб-разработка",
            "teacher": "Петров Петр Петрович",
            "exam_type": "Зачёт",
            "grade": 4,
            "semester": 2,
            "date": "2024-06-20",
            "academic_year": "2023-2024",
        },
        {
            "id": "24",
            "subject": "Мобильная разработка",
            "teacher": "Ковалев Денис Олегович",
            "exam_type": "Экзамен",
            "grade": 5,
            "semester": 2,
            "date": "2024-06-22",
            "academic_year": "2023-2024",
        },
        {
            "id": "25",
            "subject": "Машинное обучение",
            "teacher": "Семенов Артем Витальевич",
            "exam_type": "Экзамен",
            "grade": 4,
            "semester": 2,
            "date": "2024-06-25",
            "academic_year": "2023-2024",
        },
        {
            "id": "26",
            "subject": "Кибербезопасность",
            "teacher": "Медведев Роман Игоревич",
            "exam_type": "Экзамен",
            "grade": 5,
            "semester": 2,
            "date": "2024-06-28",
            "academic_year": "2023-2024",
        },
        {
            "id": "27",
            "subject": "Компьютерные сети",
            "teacher": "Носов Владимир Александрович",
            "exam_type": "Экзамен",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-01",
            "academic_year": "2023-2024",
        },
        {
            "id": "28",
            "subject": "Разработка игр",
            "teacher": "Ларин Евгений Дмитриевич",
            "exam_type": "Зачёт",
            "grade": 5,
            "semester": 2,
            "date": "2024-07-03",
            "academic_year": "2023-2024",
        },
        {
            "id": "29",
            "subject": "Базы данных (продвинутый курс)",
            "teacher": "Иванов Иван Иванович",
            "exam_type": "Экзамен",
            "grade": 5,
            "semester": 2,
            "date": "2024-07-05",
            "academic_year": "2023-2024",
        },
        {
            "id": "30",
            "subject": "Тестирование программного обеспечения",
            "teacher": "Зайцева Мария Сергеевна",
            "exam_type": "Зачёт",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-08",
            "academic_year": "2023-2024",
        },
        {
            "id": "31",
            "subject": "Проектирование интерфейсов",
            "teacher": "Воробьева Екатерина Андреевна",
            "exam_type": "Зачёт",
            "grade": 5,
            "semester": 2,
            "date": "2024-07-10",
            "academic_year": "2023-2024",
        },
        {
            "id": "32",
            "subject": "Распределенные системы",
            "teacher": "Степанов Константин Викторович",
            "exam_type": "Экзамен",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-12",
            "academic_year": "2023-2024",
        },
        {
            "id": "33",
            "subject": "Компьютерная лингвистика",
            "teacher": "Михайлова Анна Павловна",
            "exam_type": "Зачёт",
            "grade": 3,
            "semester": 2,
            "date": "2024-07-15",
            "academic_year": "2023-2024",
        },
        {
            "id": "34",
            "subject": "Блокчейн технологии",
            "teacher": "Тарасов Дмитрий Николаевич",
            "exam_type": "Экзамен",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-18",
            "academic_year": "2023-2024",
        },
        {
            "id": "35",
            "subject": "Облачные вычисления",
            "teacher": "Филиппов Алексей Сергеевич",
            "exam_type": "Экзамен",
            "grade": 5,
            "semester": 2,
            "date": "2024-07-20",
            "academic_year": "2023-2024",
        },
        {
            "id": "36",
            "subject": "Параллельное программирование",
            "teacher": "Данилов Игорь Владимирович",
            "exam_type": "Экзамен",
            "grade": 3,
            "semester": 2,
            "date": "2024-07-22",
            "academic_year": "2023-2024",
        },
        {
            "id": "37",
            "subject": "Веб-дизайн",
            "teacher": "Антонова Светлана Игоревна",
            "exam_type": "Зачёт",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-25",
            "academic_year": "2023-2024",
        },
        {
            "id": "38",
            "subject": "Искусственный интеллект",
            "teacher": "Семенов Артем Витальевич",
            "exam_type": "Экзамен",
            "grade": 5,
            "semester": 2,
            "date": "2024-07-28",
            "academic_year": "2023-2024",
        },
        {
            "id": "39",
            "subject": "Методы оптимизации",
            "teacher": "Григорьев Александр Петрович",
            "exam_type": "Экзамен",
            "grade": 4,
            "semester": 2,
            "date": "2024-07-30",
            "academic_year": "2023-2024",
        },
        {
            "id": "40",
            "subject": "Управление проектами",
            "teacher": "Аметов Осман Мидатович",
            "exam_type": "Зачёт",
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
    print(f"Инициализировано {len(initial_data)} записей в БД (gradebook)")


async def init_schedule_data(db: AsyncSession):
    """Заполнение БД начальными данными расписания (~50 записей). day_of_week: 1=Пн .. 7=Вс"""
    result = await db.execute(select(ScheduleItemDB))
    existing = result.scalars().all()
    if existing:
        print("Данные расписания уже существуют в БД, пропускаем инициализацию")
        return

    initial_data = [
        {"id": "s1", "subject": "ООП", "teacher": "Сейдаметов Гирей Серверович", "day_of_week": 1, "start_time": "08:00", "end_time": "09:30", "room": "ауд. 301", "group_id": "ИС-41", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s2", "subject": "Математический анализ", "teacher": "Григорьев Александр Петрович", "day_of_week": 1, "start_time": "09:45", "end_time": "11:15", "room": "ауд. 205", "group_id": "ИС-41", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s3", "subject": "Базы данных", "teacher": "Иванов Иван Иванович", "day_of_week": 1, "start_time": "11:30", "end_time": "13:00", "room": "ауд. 412", "group_id": "ИС-41", "lesson_type": "Практика", "week_type": "odd"},
        {"id": "s4", "subject": "Веб-разработка", "teacher": "Петров Петр Петрович", "day_of_week": 1, "start_time": "13:50", "end_time": "15:20", "room": "ауд. 318", "group_id": "ИС-42", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s5", "subject": "Алгоритмы и структуры данных", "teacher": "Сидоров Сидор Сидорович", "day_of_week": 1, "start_time": "15:35", "end_time": "17:05", "room": "ауд. 301", "group_id": "ИС-42", "lesson_type": "Практика", "week_type": "even"},
        {"id": "s6", "subject": "Дискретная математика", "teacher": "Козлова Мария Петровна", "day_of_week": 2, "start_time": "08:00", "end_time": "09:30", "room": "ауд. 102", "group_id": "ИС-41", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s7", "subject": "Проектный практикум", "teacher": "Аметов Осман Мидатович", "day_of_week": 2, "start_time": "09:45", "end_time": "11:15", "room": "ауд. 401", "group_id": "ИС-41", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s8", "subject": "Математическая логика", "teacher": "Абдураманов Зиннур Шевкетович", "day_of_week": 2, "start_time": "11:30", "end_time": "13:00", "room": "ауд. 205", "group_id": "ИС-41", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s9", "subject": "Системное программирование", "teacher": "Абдураманов Зиннур Шевкетович", "day_of_week": 2, "start_time": "13:50", "end_time": "15:20", "room": "ауд. 312", "group_id": "ПИ-31", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s10", "subject": "Операционные системы", "teacher": "Романов Виктор Иванович", "day_of_week": 2, "start_time": "15:35", "end_time": "17:05", "room": "ауд. 318", "group_id": "ПИ-31", "lesson_type": "Лаб. работа", "week_type": "odd"},
        {"id": "s11", "subject": "Иностранный язык", "teacher": "Смирнова Елена Александровна", "day_of_week": 3, "start_time": "08:00", "end_time": "09:30", "room": "ауд. 201", "group_id": "ИС-41", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s12", "subject": "Линейная алгебра", "teacher": "Морозов Сергей Николаевич", "day_of_week": 3, "start_time": "09:45", "end_time": "11:15", "room": "ауд. 103", "group_id": "ИС-41", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s13", "subject": "Программирование на Python", "teacher": "Лебедев Андрей Викторович", "day_of_week": 3, "start_time": "11:30", "end_time": "13:00", "room": "ауд. 412", "group_id": "ИС-41", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s14", "subject": "Компьютерные сети", "teacher": "Носов Владимир Александрович", "day_of_week": 3, "start_time": "13:50", "end_time": "15:20", "room": "ауд. 305", "group_id": "ИС-42", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s15", "subject": "Кибербезопасность", "teacher": "Медведев Роман Игоревич", "day_of_week": 3, "start_time": "15:35", "end_time": "17:05", "room": "ауд. 318", "group_id": "ИС-42", "lesson_type": "Практика", "week_type": "even"},
        {"id": "s16", "subject": "Теория вероятностей", "teacher": "Орлов Павел Алексеевич", "day_of_week": 4, "start_time": "08:00", "end_time": "09:30", "room": "ауд. 205", "group_id": "ИС-41", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s17", "subject": "Архитектура компьютеров", "teacher": "Федоров Игорь Борисович", "day_of_week": 4, "start_time": "09:45", "end_time": "11:15", "room": "ауд. 301", "group_id": "ИС-41", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s18", "subject": "Мобильная разработка", "teacher": "Ковалев Денис Олегович", "day_of_week": 4, "start_time": "11:30", "end_time": "13:00", "room": "ауд. 412", "group_id": "ИС-42", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s19", "subject": "Машинное обучение", "teacher": "Семенов Артем Витальевич", "day_of_week": 4, "start_time": "13:50", "end_time": "15:20", "room": "ауд. 318", "group_id": "ИС-42", "lesson_type": "Лекция", "week_type": "odd"},
        {"id": "s20", "subject": "Экономика", "teacher": "Кузнецова Ольга Дмитриевна", "day_of_week": 4, "start_time": "15:35", "end_time": "17:05", "room": "ауд. 102", "group_id": "ПИ-31", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s21", "subject": "Физкультура", "teacher": "Ткачев Иван Сергеевич", "day_of_week": 5, "start_time": "08:00", "end_time": "09:30", "room": "Спортзал", "group_id": "ИС-41", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s22", "subject": "Компьютерная графика", "teacher": "Соколова Наталья Сергеевна", "day_of_week": 5, "start_time": "09:45", "end_time": "11:15", "room": "ауд. 412", "group_id": "ИС-41", "lesson_type": "Лаб. работа", "week_type": "even"},
        {"id": "s23", "subject": "Сетевые технологии", "teacher": "Белов Максим Андреевич", "day_of_week": 5, "start_time": "11:30", "end_time": "13:00", "room": "ауд. 305", "group_id": "ИС-41", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s24", "subject": "Разработка игр", "teacher": "Ларин Евгений Дмитриевич", "day_of_week": 5, "start_time": "13:50", "end_time": "15:20", "room": "ауд. 401", "group_id": "ИС-42", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s25", "subject": "Тестирование ПО", "teacher": "Зайцева Мария Сергеевна", "day_of_week": 5, "start_time": "15:35", "end_time": "17:05", "room": "ауд. 318", "group_id": "ИС-42", "lesson_type": "Практика", "week_type": "odd"},
        {"id": "s26", "subject": "Распределенные системы", "teacher": "Степанов Константин Викторович", "day_of_week": 5, "start_time": "17:20", "end_time": "18:50", "room": "ауд. 312", "group_id": "ПИ-31", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s27", "subject": "ООП", "teacher": "Сейдаметов Гирей Серверович", "day_of_week": 1, "start_time": "08:00", "end_time": "09:30", "room": "ауд. 301", "group_id": "ПИ-31", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s28", "subject": "Базы данных", "teacher": "Иванов Иван Иванович", "day_of_week": 1, "start_time": "09:45", "end_time": "11:15", "room": "ауд. 412", "group_id": "ПИ-31", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s29", "subject": "История", "teacher": "Петрова Анна Игоревна", "day_of_week": 2, "start_time": "08:00", "end_time": "09:30", "room": "ауд. 102", "group_id": "ПИ-31", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s30", "subject": "Информатика", "teacher": "Новиков Алексей Владимирович", "day_of_week": 2, "start_time": "11:30", "end_time": "13:00", "room": "ауд. 318", "group_id": "ПИ-31", "lesson_type": "Лаб. работа", "week_type": "even"},
        {"id": "s31", "subject": "Искусственный интеллект", "teacher": "Семенов Артем Витальевич", "day_of_week": 3, "start_time": "13:50", "end_time": "15:20", "room": "ауд. 401", "group_id": "ПИ-31", "lesson_type": "Лекция", "week_type": "odd"},
        {"id": "s32", "subject": "Облачные вычисления", "teacher": "Филиппов Алексей Сергеевич", "day_of_week": 4, "start_time": "08:00", "end_time": "09:30", "room": "ауд. 305", "group_id": "ПИ-31", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s33", "subject": "Параллельное программирование", "teacher": "Данилов Игорь Владимирович", "day_of_week": 4, "start_time": "11:30", "end_time": "13:00", "room": "ауд. 412", "group_id": "ПИ-31", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s34", "subject": "Веб-дизайн", "teacher": "Антонова Светлана Игоревна", "day_of_week": 5, "start_time": "08:00", "end_time": "09:30", "room": "ауд. 318", "group_id": "ПИ-31", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s35", "subject": "Физика", "teacher": "Волков Дмитрий Сергеевич", "day_of_week": 6, "start_time": "09:45", "end_time": "11:15", "room": "ауд. 105", "group_id": "ИС-41", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s36", "subject": "Проектирование интерфейсов", "teacher": "Воробьева Екатерина Андреевна", "day_of_week": 6, "start_time": "11:30", "end_time": "13:00", "room": "ауд. 412", "group_id": "ИС-41", "lesson_type": "Практика", "week_type": "odd"},
        {"id": "s37", "subject": "Компьютерная лингвистика", "teacher": "Михайлова Анна Павловна", "day_of_week": 6, "start_time": "13:50", "end_time": "15:20", "room": "ауд. 201", "group_id": "ИС-42", "lesson_type": "Лекция", "week_type": "even"},
        {"id": "s38", "subject": "Блокчейн технологии", "teacher": "Тарасов Дмитрий Николаевич", "day_of_week": 6, "start_time": "15:35", "end_time": "17:05", "room": "ауд. 318", "group_id": "ИС-42", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s39", "subject": "Методы оптимизации", "teacher": "Григорьев Александр Петрович", "day_of_week": 6, "start_time": "08:00", "end_time": "09:30", "room": "ауд. 205", "group_id": "ПИ-31", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s40", "subject": "Управление проектами", "teacher": "Аметов Осман Мидатович", "day_of_week": 6, "start_time": "09:45", "end_time": "11:15", "room": "ауд. 301", "group_id": "ПИ-31", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s41", "subject": "ООП", "teacher": "Сейдаметов Гирей Серверович", "day_of_week": 2, "start_time": "13:50", "end_time": "15:20", "room": "ауд. 301", "group_id": "ИС-42", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s42", "subject": "Математический анализ", "teacher": "Григорьев Александр Петрович", "day_of_week": 3, "start_time": "08:00", "end_time": "09:30", "room": "ауд. 103", "group_id": "ИС-42", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s43", "subject": "Веб-разработка", "teacher": "Петров Петр Петрович", "day_of_week": 4, "start_time": "11:30", "end_time": "13:00", "room": "ауд. 318", "group_id": "ИС-41", "lesson_type": "Практика", "week_type": "even"},
        {"id": "s44", "subject": "Алгоритмы и структуры данных", "teacher": "Сидоров Сидор Сидорович", "day_of_week": 5, "start_time": "11:30", "end_time": "13:00", "room": "ауд. 301", "group_id": "ПИ-31", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s45", "subject": "Дискретная математика", "teacher": "Козлова Мария Петровна", "day_of_week": 1, "start_time": "13:50", "end_time": "15:20", "room": "ауд. 102", "group_id": "ПИ-31", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s46", "subject": "Линейная алгебра", "teacher": "Морозов Сергей Николаевич", "day_of_week": 2, "start_time": "15:35", "end_time": "17:05", "room": "ауд. 103", "group_id": "ИС-42", "lesson_type": "Лекция", "week_type": "all"},
        {"id": "s47", "subject": "Иностранный язык", "teacher": "Смирнова Елена Александровна", "day_of_week": 3, "start_time": "15:35", "end_time": "17:05", "room": "ауд. 201", "group_id": "ИС-42", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s48", "subject": "Теория вероятностей", "teacher": "Орлов Павел Алексеевич", "day_of_week": 4, "start_time": "15:35", "end_time": "17:05", "room": "ауд. 205", "group_id": "ИС-41", "lesson_type": "Практика", "week_type": "odd"},
        {"id": "s49", "subject": "Физкультура", "teacher": "Ткачев Иван Сергеевич", "day_of_week": 5, "start_time": "08:00", "end_time": "09:30", "room": "Спортзал", "group_id": "ИС-42", "lesson_type": "Практика", "week_type": "all"},
        {"id": "s50", "subject": "Физкультура", "teacher": "Ткачев Иван Сергеевич", "day_of_week": 6, "start_time": "15:35", "end_time": "17:05", "room": "Спортзал", "group_id": "ПИ-31", "lesson_type": "Практика", "week_type": "all"},
    ]

    for data in initial_data:
        db.add(ScheduleItemDB(**data))
    await db.commit()
    print(f"Инициализировано {len(initial_data)} записей в БД (schedule)")


async def init_news_data(db: AsyncSession):
    """Заполнение БД начальными новостями."""
    result = await db.execute(select(NewsDB))
    if result.scalars().first():
        print("Данные новостей уже существуют в БД, пропускаем инициализацию")
        return

    def dt(s: str) -> str:
        return s  # ISO 8601 строки как есть

    initial_data = [
        {"id": "n1", "message_id": "msg_001", "title": "Добро пожаловать в приложение университета", "text": "Теперь вы можете просматривать расписание, оценки и новости в одном месте. Желаем успехов в учёбе!", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-01T10:00:00.000Z"), "created_at": dt("2024-09-01T09:00:00.000Z"), "updated_at": dt("2024-09-01T09:00:00.000Z")},
        {"id": "n2", "message_id": "msg_002", "title": "Начало учебного года 2024/25", "text": "Учебные занятия начинаются 2 сентября. Расписание доступно в разделе «Расписание». Обратите внимание на изменения в аудиториях.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-08-28T12:00:00.000Z"), "created_at": dt("2024-08-28T11:00:00.000Z"), "updated_at": dt("2024-08-28T11:00:00.000Z")},
        {"id": "n3", "message_id": "msg_003", "title": "Запись на курсы по выбору", "text": "С 5 по 15 сентября открыта запись на дисциплины по выбору. Выберите курсы в личном кабинете до указанной даты.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-04T08:00:00.000Z"), "created_at": dt("2024-09-04T07:30:00.000Z"), "updated_at": dt("2024-09-04T07:30:00.000Z")},
        {"id": "n4", "message_id": "msg_004", "title": "Родительское собрание", "text": "Родительское собрание для студентов 1 курса состоится 10 сентября в 18:00 в актовом зале. Приглашаются родители и опекуны.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-08T14:00:00.000Z"), "created_at": dt("2024-09-08T13:00:00.000Z"), "updated_at": dt("2024-09-08T13:00:00.000Z")},
        {"id": "n5", "message_id": "msg_005", "title": "Олимпиада по программированию", "text": "В октябре пройдёт внутривузовская олимпиада по программированию. Регистрация до 1 октября. Подробности на кафедре информатики.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-15T09:00:00.000Z"), "created_at": dt("2024-09-15T08:00:00.000Z"), "updated_at": dt("2024-09-15T08:00:00.000Z")},
        {"id": "n6", "message_id": "msg_006", "title": "Изменение расписания на 20 сентября", "text": "В понедельник 20 сентября пары по математическому анализу для группы ИС-41 переносятся с 3-й на 5-ю пару. Аудитория не меняется.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-18T16:00:00.000Z"), "created_at": dt("2024-09-18T15:00:00.000Z"), "updated_at": dt("2024-09-18T15:00:00.000Z")},
        {"id": "n7", "message_id": "msg_007", "title": "Библиотека: новые поступления", "text": "В библиотеку поступили учебники по машинному обучению и веб-разработке. Список доступен на сайте библиотеки. Выдача по студенческому.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-20T11:00:00.000Z"), "created_at": dt("2024-09-20T10:00:00.000Z"), "updated_at": dt("2024-09-20T10:00:00.000Z")},
        {"id": "n8", "message_id": "msg_008", "title": "Спортивные секции", "text": "Открыта запись в секции: волейбол, баскетбол, шахматы, плавание. Тренировки начинаются с 23 сентября. Запись в спорткомплексе.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-21T08:00:00.000Z"), "created_at": dt("2024-09-21T07:00:00.000Z"), "updated_at": dt("2024-09-21T07:00:00.000Z")},
        {"id": "n9", "message_id": "msg_009", "title": "Вебинар от партнёров", "text": "Компания-партнёр проведёт вебинар «Карьера в IT» 25 сентября в 15:00. Ссылка на подключение будет в рассылке. Регистрация обязательна.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-22T12:00:00.000Z"), "created_at": dt("2024-09-22T11:00:00.000Z"), "updated_at": dt("2024-09-22T11:00:00.000Z")},
        {"id": "n10", "message_id": "msg_010", "title": "Декада науки", "text": "С 1 по 10 октября в университете проходит декада науки. Студентов приглашают на лекции и мастер-классы. Программа на стендах и на сайте.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-25T10:00:00.000Z"), "created_at": dt("2024-09-25T09:00:00.000Z"), "updated_at": dt("2024-09-25T09:00:00.000Z")},
        {"id": "n11", "message_id": "msg_011", "title": "Технические работы в ЛК", "text": "28 сентября с 02:00 до 06:00 будут проводиться технические работы в личном кабинете. В этот период вход может быть недоступен. Приносим извинения.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-26T14:00:00.000Z"), "created_at": dt("2024-09-26T13:00:00.000Z"), "updated_at": dt("2024-09-26T13:00:00.000Z")},
        {"id": "n12", "message_id": "msg_012", "title": "Стипендия: сроки перечисления", "text": "Стипендия за сентябрь будет перечислена до 10 октября. Проверьте реквизиты в личном кабинете. Вопросы — в отделе стипендий.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-09-27T09:00:00.000Z"), "created_at": dt("2024-09-27T08:00:00.000Z"), "updated_at": dt("2024-09-27T08:00:00.000Z")},
        {"id": "n13", "message_id": "msg_013", "title": "Консультации перед сессией", "text": "С 15 октября преподаватели проводят консультации перед осенней сессией. График консультаций вывешен на кафедрах и в приложении.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-10-01T11:00:00.000Z"), "created_at": dt("2024-10-01T10:00:00.000Z"), "updated_at": dt("2024-10-01T10:00:00.000Z")},
        {"id": "n14", "message_id": "msg_014", "title": "День открытых дверей", "text": "12 октября — день открытых дверей для абитуриентов. Студентов приглашают помочь в организации и рассказать об учёбе. Заявки принимаются до 8 октября.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-10-03T15:00:00.000Z"), "created_at": dt("2024-10-03T14:00:00.000Z"), "updated_at": dt("2024-10-03T14:00:00.000Z")},
        {"id": "n15", "message_id": "msg_015", "title": "Обновление мобильного приложения", "text": "Вышла новая версия приложения университета: добавлены уведомления о расписании и новости. Обновите приложение в магазине.", "image_urls": json.dumps([]), "media_group_id": None, "published_at": dt("2024-10-05T12:00:00.000Z"), "created_at": dt("2024-10-05T11:00:00.000Z"), "updated_at": dt("2024-10-05T11:00:00.000Z")},
    ]

    for data in initial_data:
        db.add(NewsDB(**data))
    await db.commit()
    print(f"Инициализировано {len(initial_data)} записей в БД (news)")


