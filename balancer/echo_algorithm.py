# -*- coding: utf-8 -*-
"""
Алгоритм "Эхо" для сбора данных о нагрузке по дереву.
Инициатор (master) отправляет маркеры всем соседям, волна распространяется до листьев,
листья возвращают эхо с данными, промежуточные узлы собирают эхо от детей и передают родителю.
"""
import asyncio
from typing import Dict, Optional, List
from balancer.config import TREE, get_node_url
import httpx


async def echo_algorithm_collect_load(initiator_id: str = "master", host: str = "127.0.0.1") -> Dict[str, int]:
    """
    Алгоритм "Эхо": сбор нагрузки от всех узлов через волну маркеров.
    
    Процесс для инициатора:
    1. Отправить маркер всем соседям (Out(this))
    2. Ждать эхо от всех соседей (counter < card(Out(this)))
    3. Получить все данные, вернуть OK
    
    Процесс для не-инициаторов:
    1. Получить маркер от u, запомнить pre(this) = u
    2. Отправить маркер всем соседям кроме pre(this)
    3. Ждать эхо от всех детей
    4. Вернуть эхо родителю pre(this) с данными о нагрузке
    
    Возвращает словарь node_id -> load.
    """
    result = {}
    
    async def send_token_to_children(node_id: str, exclude: Optional[str] = None) -> Dict[str, int]:
        """Отправить маркер всем детям (кроме exclude) и собрать эхо."""
        node_info = TREE[node_id]
        children = [c for c in node_info["children"] if c != exclude]
        if not children:
            # Лист: вернуть свою нагрузку
            if node_info["type"] == "leaf":
                load = await get_node_load(node_id, host)
                return {node_id: load}
            return {}
        
        # Отправить маркер всем детям
        child_results = {}
        async with httpx.AsyncClient(timeout=5.0) as client:
            tasks = []
            for child_id in children:
                url = f"{get_node_url(child_id, host)}/echo_token"
                tasks.append(client.post(url, json={"from": node_id}))
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            for child_id, resp in zip(children, responses):
                if isinstance(resp, Exception) or resp.status_code != 200:
                    child_results[child_id] = -1
                else:
                    data = resp.json()
                    child_results.update(data.get("loads", {}))
        
        return child_results
    
    async def get_node_load(node_id: str, host: str) -> int:
        """Получить нагрузку узла (для листьев — от воркера, для промежуточных — сумма детей)."""
        node_info = TREE[node_id]
        if node_info["type"] == "leaf":
            url = f"{get_node_url(node_id, host)}/load"
            try:
                async with httpx.AsyncClient(timeout=2.0) as client:
                    r = await client.get(url)
                    if r.status_code == 200:
                        return r.json().get("load", 0)
            except Exception:
                pass
            return -1
        return 0  # для промежуточных узлов нагрузка = сумма детей
    
    # Инициатор: отправить маркер всем соседям и собрать эхо
    initiator_info = TREE[initiator_id]
    children = initiator_info["children"]
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = []
        for child_id in children:
            url = f"{get_node_url(child_id, host)}/echo_token"
            tasks.append(client.post(url, json={"from_node": initiator_id}))
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for child_id, resp in zip(children, responses):
            if isinstance(resp, Exception) or resp.status_code != 200:
                # Если промежуточный узел недоступен, помечаем его и всех детей как -1
                result[child_id] = -1
                for grandchild in TREE.get(child_id, {}).get("children", []):
                    result[grandchild] = -1
            else:
                data = resp.json()
                result.update(data.get("loads", {}))
    
    return result


async def collect_load_from_workers(host: str = "127.0.0.1") -> Dict[str, int]:
    """
    Упрощённый сбор только с воркеров (для обратной совместимости).
    Использует алгоритм "Эхо" для сбора данных.
    """
    all_loads = await echo_algorithm_collect_load("master", host)
    # Фильтруем только воркеры (листья)
    from balancer.config import get_all_workers
    workers = get_all_workers()
    return {w: all_loads.get(w, -1) for w in workers}
