#!/bin/bash
# Полная демонстрация: запуск всех узлов, нагружение, балансировка, визуализация
# Запускать из корня проекта: back_uni/

cd "$(dirname "$0")/.."

echo "=== Шаг 1: Запуск всех узлов ==="
echo "Запускаем группы и воркеры в фоне..."
./balancer/start_all.sh
sleep 2

echo ""
echo "=== Шаг 2: Запуск мастера (в фоне) ==="
python3 -m uvicorn balancer.master:app --host 0.0.0.0 --port 9000 &
MASTER_PID=$!
sleep 3

echo ""
echo "=== Шаг 3: Проверка доступности ==="
curl -s http://127.0.0.1:9000/loads | python3 -m json.tool || echo "Мастер ещё не готов, подождите..."

echo ""
echo "=== Шаг 4: Создание визуализации ДО ==="
python3 balancer/visualize_table.py до

echo ""
echo "=== Шаг 5: Нагружение воркера 8001 ==="
python3 balancer/flood_one.py 8001 10
sleep 2

echo ""
echo "=== Шаг 6: Запуск балансировки ==="
curl http://127.0.0.1:9000/balance
sleep 5

echo ""
echo "=== Шаг 7: Создание визуализации ПОСЛЕ ==="
python3 balancer/visualize_table.py после

echo ""
echo "✅ Демонстрация завершена!"
echo "Файлы визуализации:"
echo "  - balancer/balancer_visualization_до_балансировки.html"
echo "  - balancer/balancer_visualization_после_балансировки.html"
echo ""
echo "Остановить все процессы:"
echo "  kill $MASTER_PID"
echo "  pkill -f 'balancer.(group|worker)'"
