# University Backend API

Backend API для мобильного приложения университета, написанный на Python с использованием FastAPI.

## Структура проекта

```
back_uni/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Главный файл приложения
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── gradebook.py    # API роуты для зачетной книжки
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py       # Подключение к БД
│   │   ├── models.py            # SQLAlchemy модели
│   │   └── init_data.py         # Инициализация данных
│   ├── models/
│   │   ├── __init__.py
│   │   └── grade_record.py     # Pydantic модели данных
│   ├── services/
│   │   ├── __init__.py
│   │   └── gradebook_service.py # Бизнес-логика
│   └── repositories/
│       ├── __init__.py
│       └── gradebook_repository.py # Работа с БД
├── requirements.txt
├── run.py                       # Скрипт для запуска
└── README.md
```

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск сервера

```bash
python run.py
# или
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Сервер будет доступен по адресу: `http://localhost:8000`

**Примечание:** При первом запуске автоматически создается база данных SQLite (`university.db`) и заполняется начальными данными.

### 3. Документация API

После запуска сервера доступна интерактивная документация:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Gradebook (Зачетная книжка)

#### Получить все оценки
```
GET /api/v1/gradebook/grades
```

#### Получить оценки по семестру
```
GET /api/v1/gradebook/grades?semester={semester}
```

#### Получить оценки по предмету
```
GET /api/v1/gradebook/grades?subject={subject}
```

#### Получить средний балл
```
GET /api/v1/gradebook/grades/average
```

Ответ:
```json
{
  "average": 3.88
}
```

#### Получить статистику по оценкам
```
GET /api/v1/gradebook/grades/statistics
```

Ответ:
```json
{
  "statistics": {
    "2": 1,
    "3": 2,
    "4": 2,
    "5": 3
  }
}
```

## База данных

Проект использует **SQLite** для локального хранения данных. База данных создается автоматически при первом запуске приложения в файле `university.db`.

### Инициализация данных

При первом запуске приложения автоматически:
1. Создаются таблицы в БД
2. Заполняются начальные данные (8 записей оценок)

Данные хранятся в таблице `grade_records` со следующими полями:
- `id` - уникальный идентификатор
- `subject` - название предмета
- `teacher` - ФИО преподавателя
- `exam_type` - тип экзамена (Экзамен/Зачёт)
- `grade` - оценка (2-5)
- `semester` - номер семестра
- `date` - дата сдачи
- `academic_year` - учебный год

## Архитектура

Проект использует многослойную архитектуру:

1. **API Layer** (`app/api/`) - HTTP роуты и обработка запросов
2. **Service Layer** (`app/services/`) - Бизнес-логика
3. **Repository Layer** (`app/repositories/`) - Работа с БД
4. **Database Layer** (`app/database/`) - Модели БД (SQLAlchemy)
5. **Models** (`app/models/`) - Pydantic модели для API

Такая структура позволяет легко добавлять новые модули (например, расписание, новости и т.д.) по аналогии с модулем gradebook.

## Добавление новых модулей

Для добавления нового модуля (например, "schedule"):

1. Создать модель в `app/models/schedule.py`
2. Создать репозиторий в `app/repositories/schedule_repository.py`
3. Создать сервис в `app/services/schedule_service.py`
4. Создать роуты в `app/api/v1/schedule.py`
5. Подключить роутер в `app/main.py`

## Технологии

- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy** - ORM для работы с БД
- **SQLite** - локальная база данных
- **Pydantic** - валидация данных
- **Uvicorn** - ASGI сервер
- **Python 3.8+**

## CORS

По умолчанию CORS настроен на разрешение всех источников (`allow_origins=["*"]`). В продакшене рекомендуется указать конкретные домены мобильного приложения.

# uni_dev_back
