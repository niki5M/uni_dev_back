"""Скрипт «завалить» один воркер запросами для демонстрации балансировки."""
import sys
import httpx


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    url = f"http://127.0.0.1:{port}/tasks"
    with httpx.Client() as client:
        for i in range(count):
            r = client.post(url, json={"type": "gradebook"})
            print(f" POST {url} -> {r.status_code}")
    print(f"Отправлено {count} задач на воркер :{port}. Через ~5 сек мастер перераспределит часть.")


if __name__ == "__main__":
    main()
