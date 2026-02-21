#!/bin/bash
# Запуск трёх воркеров на портах 8001, 8002, 8003 (каждый в фоне).
# Запускать из корня проекта: back_uni/
cd "$(dirname "$0")/.."
echo "Запуск воркеров на портах 8001, 8002, 8003..."
WORKER_NODE_ID=worker_8001 python -m uvicorn balancer.worker:app --host 0.0.0.0 --port 8001 &
WORKER_NODE_ID=worker_8002 python -m uvicorn balancer.worker:app --host 0.0.0.0 --port 8002 &
WORKER_NODE_ID=worker_8003 python -m uvicorn balancer.worker:app --host 0.0.0.0 --port 8003 &
echo "Воркеры запущены. Остановить: pkill -f 'balancer.worker'"
echo "Мастер запускайте отдельно: python -m uvicorn balancer.master:app --host 0.0.0.0 --port 9000"
