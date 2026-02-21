#!/bin/bash
# Проверка доступности всех узлов
# Запускать из корня проекта: back_uni/

echo "Проверка доступности узлов..."
echo ""

echo "Мастер (9000):"
curl -s http://127.0.0.1:9000/health && echo "" || echo "❌ Недоступен"
echo ""

echo "Группы:"
curl -s http://127.0.0.1:9001/health && echo "" || echo "❌ group_A (9001) недоступен"
curl -s http://127.0.0.1:9002/health && echo "" || echo "❌ group_B (9002) недоступен"
curl -s http://127.0.0.1:9003/health && echo "" || echo "❌ group_C (9003) недоступен"
echo ""

echo "Воркеры:"
for port in 8001 8002 8003 8004 8005 8006; do
    curl -s http://127.0.0.1:$port/health > /dev/null && echo "✅ worker_$port доступен" || echo "❌ worker_$port недоступен"
done
echo ""

echo "Нагрузки (от мастера):"
curl -s http://127.0.0.1:9000/loads | python3 -m json.tool 2>/dev/null || echo "Мастер не отвечает"
