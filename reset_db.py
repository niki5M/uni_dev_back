#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для пересоздания БД с новыми данными
"""
import asyncio
import os
from app.database.connection import init_db, AsyncSessionLocal, engine
from app.database.init_data import init_gradebook_data, init_schedule_data, init_news_data


async def reset_database():
    """Удаляет старую БД и создает новую с данными"""
    
    # Удаляем старую БД если существует
    db_file = "university.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Удален файл БД: {db_file}")
    
    # Создаем новую БД
    print("Создание новой БД...")
    await init_db()
    
    # Заполняем данными
    print("Заполнение данными...")
    async with AsyncSessionLocal() as db:
        await init_gradebook_data(db)
        await init_schedule_data(db)
        await init_news_data(db)
    
    print("БД успешно пересоздана с новыми данными!")


if __name__ == "__main__":
    asyncio.run(reset_database())


