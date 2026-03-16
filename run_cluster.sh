#!/usr/bin/env bash
cd "$(dirname "$0")"

# При необходимости раскомментируй строку ниже, если используешь venv:
# source venv/bin/activate

# Воркеры (листья)
python3 -m balancer.worker --port 8001 &
python3 -m balancer.worker --port 8002 &
python3 -m balancer.worker --port 8003 &
python3 -m balancer.worker --port 8004 &
python3 -m balancer.worker --port 8005 &
python3 -m balancer.worker --port 8006 &

# Группы
python3 -m balancer.group --port 9001 &
python3 -m balancer.group --port 9002 &
python3 -m balancer.group --port 9003 &

# Мастер (инициатор, центральный узел балансировки)
python3 -m balancer.master &

