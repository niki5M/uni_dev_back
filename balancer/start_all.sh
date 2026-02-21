#!/bin/bash
# Скрипт запуска всех узлов для демонстрации алгоритма "Эхо"
# Запускать из корня проекта: back_uni/

cd "$(dirname "$0")/.."

echo "Запуск промежуточных узлов (группы) на портах 9001, 9002, 9003..."
GROUP_NODE_ID=group_A python3 -m uvicorn balancer.group:app --host 0.0.0.0 --port 9001 &
GROUP_NODE_ID=group_B python3 -m uvicorn balancer.group:app --host 0.0.0.0 --port 9002 &
GROUP_NODE_ID=group_C python3 -m uvicorn balancer.group:app --host 0.0.0.0 --port 9003 &

echo "Запуск воркеров (листья) на портах 8001-8006..."
WORKER_NODE_ID=worker_8001 python3 -m uvicorn balancer.worker:app --host 0.0.0.0 --port 8001 &
WORKER_NODE_ID=worker_8002 python3 -m uvicorn balancer.worker:app --host 0.0.0.0 --port 8002 &
WORKER_NODE_ID=worker_8003 python3 -m uvicorn balancer.worker:app --host 0.0.0.0 --port 8003 &
WORKER_NODE_ID=worker_8004 python3 -m uvicorn balancer.worker:app --host 0.0.0.0 --port 8004 &
WORKER_NODE_ID=worker_8005 python3 -m uvicorn balancer.worker:app --host 0.0.0.0 --port 8005 &
WORKER_NODE_ID=worker_8006 python3 -m uvicorn balancer.worker:app --host 0.0.0.0 --port 8006 &

echo "Все узлы запущены в фоне."
echo "Запустите мастера отдельно: python3 -m uvicorn balancer.master:app --host 0.0.0.0 --port 9000"
echo ""
echo "Остановить все: pkill -f 'balancer.(group|worker)'"
