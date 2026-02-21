# -*- coding: utf-8 -*-
"""
Конфигурация дерева узлов для централизованной балансировки нагрузки.
Тема: распределённая обработка запросов университетского приложения (зачётка, расписание, новости).

Топология «дерево» для алгоритма "Эхо":
                    [Master :9000]
                   /      |      \
        [Group_A:9001] [Group_B:9002] [Group_C:9003]
         /    |          /    |          /    |
    [W1:8001][W2:8002] [W3:8003][W4:8004] [W5:8005][W6:8006]

Для демонстрации алгоритма "Эхо": мастер -> группы -> воркеры (два уровня).
"""
from typing import List, Dict, Any

# Порты
MASTER_PORT = 9000
GROUP_PORTS = [9001, 9002, 9003]  # промежуточные узлы (группы)
WORKER_PORTS = [8001, 8002, 8003, 8004, 8005, 8006]  # воркеры — листья дерева

# Дерево для алгоритма "Эхо": Out(node) = children (соседи, куда можно отправить маркер)
TREE = {
    "master": {
        "parent": None,
        "children": ["group_A", "group_B", "group_C"],
        "port": MASTER_PORT,
        "type": "initiator"
    },
    "group_A": {
        "parent": "master",
        "children": ["worker_8001", "worker_8002"],
        "port": 9001,
        "type": "intermediate"
    },
    "group_B": {
        "parent": "master",
        "children": ["worker_8003", "worker_8004"],
        "port": 9002,
        "type": "intermediate"
    },
    "group_C": {
        "parent": "master",
        "children": ["worker_8005", "worker_8006"],
        "port": 9003,
        "type": "intermediate"
    },
    "worker_8001": {"parent": "group_A", "children": [], "port": 8001, "type": "leaf"},
    "worker_8002": {"parent": "group_A", "children": [], "port": 8002, "type": "leaf"},
    "worker_8003": {"parent": "group_B", "children": [], "port": 8003, "type": "leaf"},
    "worker_8004": {"parent": "group_B", "children": [], "port": 8004, "type": "leaf"},
    "worker_8005": {"parent": "group_C", "children": [], "port": 8005, "type": "leaf"},
    "worker_8006": {"parent": "group_C", "children": [], "port": 8006, "type": "leaf"},
}

def get_node_url(node_id: str, host: str = "127.0.0.1") -> str:
    """URL узла по его ID."""
    port = TREE[node_id]["port"]
    return f"http://{host}:{port}"

def get_worker_url(node_id: str, host: str = "127.0.0.1") -> str:
    """URL воркера (для обратной совместимости)."""
    return get_node_url(node_id, host)

def get_master_url(host: str = "127.0.0.1") -> str:
    return f"http://{host}:{MASTER_PORT}"

def get_all_workers() -> List[str]:
    """Список всех воркеров (листьев дерева)."""
    return [n for n, info in TREE.items() if info.get("type") == "leaf"]
