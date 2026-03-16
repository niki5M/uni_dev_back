# -*- coding: utf-8 -*-
"""
Простая модель сети для лабораторной по централизованной балансировке
с использованием волнового алгоритма Финна.

Сеть состоит из нескольких узлов (факультетов/серверов университета) с
ориентированной топологией. Алгоритм Финна (здесь реализован в упрощённом виде
как волновой обход) используется для сбора информации о нагрузке узлов,
после чего выполняется централизованное выравнивание нагрузки.
"""

import random
from typing import Dict, List


class Node:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        # начальная загрузка узла: 0 запросов
        self.load: int = 0
        self.neighbors: List["Node"] = []
        self.parent: "Node | None" = None  # для волнового алгоритма (путь распространения)

    def add_neighbor(self, node: "Node") -> None:
        self.neighbors.append(node)

    def __repr__(self) -> str:
        return f"{self.name} ({self.address}) - Load: {self.load}"


class NetworkBalancer:
    """
    Ориентированная сеть узлов и централизованный алгоритм балансировки.

    wave_algorithm_finn() — волновой обход (по мотивам алгоритма Финна) для сбора нагрузок.
    centralized_balancing() — перераспределяет нагрузку к среднему значению.
    """

    def __init__(self) -> None:
        # Узлы сети: центральный API и сервисы студенческого приложения
        self.nodes: Dict[str, Node] = {
            "A": Node("Центральный API университета", "Шлюз /api"),
            "B": Node("Сервис зачётной книжки", "Модуль /gradebook"),
            "C": Node("Сервис расписания", "Модуль /schedule"),
            "D": Node("Сервис новостей", "Модуль /news"),
            "E": Node("Сервис справочной информации", "Модуль /directory"),
        }
        self._setup_network()

    def _setup_network(self) -> None:
        # Ориентированная топология сети (пример произвольной ориентированной сети)
        self.nodes["A"].add_neighbor(self.nodes["B"])
        self.nodes["A"].add_neighbor(self.nodes["C"])
        self.nodes["B"].add_neighbor(self.nodes["D"])
        self.nodes["C"].add_neighbor(self.nodes["D"])
        self.nodes["D"].add_neighbor(self.nodes["E"])

    def add_requests(self, count: int = 1) -> None:
        """
        Смоделировать приход новых запросов от студентов.

        Для наглядности ВСЕ новые заявки идут в один и тот же сервис,
        чтобы явно показать перекос нагрузки перед балансировкой.
        """
        if count <= 0:
            return
        # Перегружаем центральный API университета (узел "A")
        self.nodes["A"].load += count

    def wave_algorithm_finn(self) -> Dict[str, int]:
        """
        Упрощённая реализация волнового алгоритма Финна:
        - начинаем с центрального узла 'A';
        - волна обходит сеть по ориентированным рёбрам;
        - для наглядности запоминаем родителя (путь) и помечаем посещённые узлы.

        Возвращает словарь: имя узла -> текущая нагрузка.
        """
        visited = set()
        queue: List[str] = ["A"]  # начинаем с центрального узла (ключ)

        while queue:
            current_key = queue.pop(0)
            if current_key in visited:
                continue
            visited.add(current_key)

            current_node = self.nodes[current_key]
            for neighbor in current_node.neighbors:
                # Ищем ключ соседа по объекту
                neighbor_key = next(
                    key for key, node in self.nodes.items() if node is neighbor
                )
                if neighbor_key not in visited:
                    neighbor.parent = current_node  # запоминаем путь распространения волны
                    queue.append(neighbor_key)

        # Возвращаем информацию о нагрузке каждого узла
        return {node.name: node.load for node in self.nodes.values()}

    def centralized_balancing(self) -> None:
        """
        Централизованный алгоритм балансировки на основе собранных данных.
        Использует результаты wave_algorithm_finn() для расчёта средней нагрузки.
        """
        loads = self.wave_algorithm_finn()
        avg_load = sum(loads.values()) // len(self.nodes)

        # Узлы с избыточной нагрузкой и узлы с дефицитом
        excess_nodes = [node for node in self.nodes.values() if node.load > avg_load]
        deficit_nodes = [node for node in self.nodes.values() if node.load < avg_load]

        for node in excess_nodes:
            while node.load > avg_load and deficit_nodes:
                deficit_node = deficit_nodes.pop(0)
                transfer = min(node.load - avg_load, avg_load - deficit_node.load)
                node.load -= transfer
                deficit_node.load += transfer
                if deficit_node.load < avg_load:
                    deficit_nodes.append(deficit_node)

    def get_network_status(self) -> Dict[str, Dict[str, int]]:
        """Текущая нагрузка узлов (для отображения на сайте)."""
        return {
            key: {"address": node.address, "load": node.load}
            for key, node in self.nodes.items()
        }


if __name__ == "__main__":
    nb = NetworkBalancer()
    print("До балансировки:", nb.get_network_status())
    nb.centralized_balancing()
    print("После балансировки:", nb.get_network_status())

