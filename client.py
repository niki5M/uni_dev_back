"""
Клиент демо-нагрузки: один запрос на мастер.
Мастер выбирает наименее загруженный узел и ставит задачу в очередь.
"""
import httpx

# Единая точка входа
MASTER_URL = "http://127.0.0.1:9000"
REGISTER_URL = f"{MASTER_URL}/register_request"


def register_request(request_type: str = "gradebook"):
    """Отправка задачи (gradebook → карточки, schedule → план, news → лента)."""
    response = httpx.post(REGISTER_URL, json={"request_type": request_type})
    if response.status_code == 200:
        data = response.json()
        print(f"{data.get('message', 'Запрос записан в ' + data.get('worker', '?'))}")
    else:
        err = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
        print(f"Ошибка: {err.get('message', response.text)}")


if __name__ == "__main__":
    print("Тип задачи: gradebook (карточки), schedule (план), news (лента)")
    request_type = input("Введите тип (по умолчанию gradebook): ").strip() or "gradebook"
    register_request(request_type)
