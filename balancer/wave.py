# -*- coding: utf-8 -*-
"""
Волновой алгоритм сбора нагрузки по дереву.
Листья отдают нагрузку родителю, промежуточные узлы суммируют и передают вверх.
В нашей топологии все воркеры — листья с общим родителем (Master), поэтому
достаточно опросить каждого воркера и собрать карту нагрузок у центра.
"""
from typing import Dict, List
from balancer.config import TREE, get_worker_url
import httpx


async def collect_load_from_workers(host: str = "127.0.0.1") -> Dict[str, int]:
    """
    Сбор нагрузки со всех воркеров (волна от листьев к корню).
    Возвращает словарь node_id -> load (-1 если узел недоступен).
    """
    worker_ids = [n for n, info in TREE.items() if info["parent"] == "master"]
    result = {n: -1 for n in worker_ids}
    async with httpx.AsyncClient(timeout=2.0) as client:
        for node_id in worker_ids:
            url = f"{get_worker_url(node_id, host)}/load"
            try:
                r = await client.get(url)
                if r.status_code == 200:
                    data = r.json()
                    result[data["node_id"]] = data["load"]
                else:
                    result[node_id] = -1
            except Exception:
                result[node_id] = -1
    return result
