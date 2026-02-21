#!/bin/bash
# Скрипт для создания визуализации до и после балансировки
# Запускать из корня проекта: back_uni/

cd "$(dirname "$0")/.."

echo "=== Создание визуализации ДО балансировки ==="
python3 balancer/visualize_table.py до

echo ""
echo "Нажмите Enter после запуска балансировки (curl http://127.0.0.1:9000/balance)..."
read

echo ""
echo "=== Создание визуализации ПОСЛЕ балансировки ==="
python3 balancer/visualize_table.py после

echo ""
echo "✅ Готово! Откройте файлы в браузере:"
echo "   - balancer/balancer_visualization_до_балансировки.html"
echo "   - balancer/balancer_visualization_после_балансировки.html"
