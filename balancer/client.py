#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Клиент для студентов: один запрос на мастер (как в примере с клиникой).
Мастер сам выбирает наименее загруженный узел и записывает туда запрос.
"""
import httpx

# Единая точка входа (как SERVER_URL = "http://127.0.0.1:5000/register_patient")
MASTER_URL = "http://127.0.0.1:9000"
REGISTER_URL = f"{MASTER_URL}/register_request"


def register_request(request_type: str = "gradebook"):
    """Отправка запроса на обработку (зачётка, расписание, новости)."""
    response = httpx.post(REGISTER_URL, json={"request_type": request_type})
    if response.status_code == 200:
        data = response.json()
        print(f"{data.get('message', 'Запрос записан в ' + data.get('worker', '?'))}")
    else:
        err = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
        print(f"Ошибка: {err.get('message', response.text)}")


if __name__ == "__main__":
    print("Тип запроса: gradebook, schedule, news")
    request_type = input("Введите тип запроса (по умолчанию gradebook): ").strip() or "gradebook"
    register_request(request_type)
