"""
Конфигурация дерева узлов для централизованной балансировки нагрузки.
Топология «дерево»:
        [Master :9000]
        /    |    \\
[W1:8001] [W2:8002] [W3:8003]
    |
[W4:8004] (опционально — второй уровень)
"""
from typing import List, Dict, Any

MASTER_PORT = 9000
WORKER_PORTS = [8001, 8002, 8003] 

TREE = {
    "master": {"parent": None, "children": ["worker_8001", "worker_8002", "worker_8003"], "port": MASTER_PORT},
    "worker_8001": {"parent": "master", "children": [], "port": 8001},
    "worker_8002": {"parent": "master", "children": [], "port": 8002},
    "worker_8003": {"parent": "master", "children": [], "port": 8003},
}


def get_worker_url(node_id: str, host: str = "127.0.0.1") -> str:
    port = TREE[node_id]["port"]
    return f"http://{host}:{port}"


def get_master_url(host: str = "127.0.0.1") -> str:
    return f"http://{host}:{MASTER_PORT}"
