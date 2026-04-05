# Notes Service API

Backend API для приложения заметок на FastAPI: карточки с приоритетом (модуль `gradebook`), план недели (`schedule`) и лента (`news`). Префиксы путей и имена полей JSON сохранены для совместимости с существующими клиентами.

## Структура проекта

```
uni_dev_back/
├── app/
│   ├── main.py
│   ├── api/v1/          # gradebook, schedule, news
│   ├── database/
│   ├── models/
│   ├── services/
│   └── repositories/
├── balancer/            # модели задач для master/worker
├── requirements.txt
├── run.py
└── README.md
```

## Установка и запуск

### 1. Зависимости

```bash
pip install -r requirements.txt
```

### 2. Сервер

```bash
python run.py
# или
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Адрес: `http://localhost:8000`

При первом запуске создаётся SQLite `university.db` и заполняется демо-данными.

### 3. Документация

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API (логика без изменений)

### Карточки заметок (`/api/v1/gradebook`)

- `GET /grades` — список; опционально `semester`, `subject`
- `GET /grades/average` — среднее по полю `grade` (приоритет)
- `GET /grades/statistics` — счётчики по значениям `grade`

Семантика полей в теме «заметки»: `subject` — заголовок, `teacher` — автор, `exam_type` — статус, `grade` — приоритет 2–5, `semester` — раздел, `academic_year` — период архива.

### План недели (`/api/v1/schedule/group-schedules` и `/api/group-schedules`)

Параметры: `day` (1–7), `group` (идентификатор пространства, например `основной`).

### Лента (`/api/v1/news`, `/api/news`)

Список и `GET /{id}` — без изменений.

## База данных

SQLite, файл `university.db` (или `DATABASE_URL`). Таблицы: `grade_records`, `schedule_items`, `news`.

Пересоздать БД с нуля:

```bash
python reset_db.py
```

## Архитектура

Слои: API → Service → Repository → БД; Pydantic-модели для ответов.

## Технологии

FastAPI, SQLAlchemy (async), SQLite, Pydantic, Uvicorn, Python 3.8+.

## CORS

По умолчанию `allow_origins=["*"]`. В продакшене задайте конкретные источники.
