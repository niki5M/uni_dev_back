from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any
import random
import uuid


@dataclass
class WaveMessage:
    sender: str
    payload: Dict[str, Tuple[int, int]]  # node_id -> (load, version)


@dataclass
class TransferMessage:
    sender: str
    amount: int


@dataclass
class NodeState:
    node_id: str
    load: int = 0
    version: int = 0
    knowledge: Dict[str, Tuple[int, int]] = field(default_factory=dict)
    in_wave: List[WaveMessage] = field(default_factory=list)
    in_transfer: List[TransferMessage] = field(default_factory=list)

    def snapshot(self) -> None:
        self.knowledge[self.node_id] = (self.load, self.version)


class DecentralizedPhaseWaveBalancer:
    """
    Децентрализованный фазовый волновой алгоритм балансировки для произвольного
    ориентированного графа.

    Фаза 1 (wave): узлы распространяют известные оценки нагрузок по всем исходящим ребрам.
    Фаза 2 (transfer): каждый узел локально решает, сколько передать по исходящим ребрам.
    """

    def __init__(self, topology: Dict[str, List[str]] | None = None):
        self.topology: Dict[str, List[str]] = topology or self._default_topology()
        self.nodes: Dict[str, NodeState] = {
            node_id: NodeState(node_id=node_id) for node_id in self.topology.keys()
        }
        self._validate_topology()

    @staticmethod
    def _default_topology() -> Dict[str, List[str]]:
        # Произвольный ориентированный граф (не дерево), есть циклы и перекрестные дуги.
        return {
            "n1": ["n2", "n3"],
            "n2": ["n3", "n4"],
            "n3": ["n5"],
            "n4": ["n1", "n5"],
            "n5": ["n2", "n6"],
            "n6": ["n3"],
        }

    def _validate_topology(self) -> None:
        all_nodes = set(self.topology.keys())
        for src, dst_list in self.topology.items():
            if src not in self.nodes:
                raise ValueError(f"Unknown source node: {src}")
            for dst in dst_list:
                if dst not in all_nodes:
                    raise ValueError(f"Edge {src}->{dst} points to unknown node")

    def _incoming_map(self) -> Dict[str, List[str]]:
        incoming: Dict[str, List[str]] = {n: [] for n in self.topology.keys()}
        for src, dsts in self.topology.items():
            for dst in dsts:
                incoming[dst].append(src)
        return incoming

    def set_topology(self, topology: Dict[str, List[str]]) -> None:
        self.topology = topology
        self.nodes = {node_id: NodeState(node_id=node_id) for node_id in self.topology.keys()}
        self._validate_topology()

    def get_status(self) -> Dict[str, Any]:
        return {
            "topology": self.topology,
            "loads": {node_id: node.load for node_id, node in self.nodes.items()},
            "total_load": sum(node.load for node in self.nodes.values()),
        }

    def set_loads(self, loads: Dict[str, int]) -> None:
        for node_id, load in loads.items():
            if node_id not in self.nodes:
                raise ValueError(f"Unknown node: {node_id}")
            self.nodes[node_id].load = max(0, int(load))
            self.nodes[node_id].version += 1
            self.nodes[node_id].snapshot()

    def add_requests(self, count: int = 10) -> Dict[str, int]:
        node_ids = list(self.nodes.keys())
        if not node_ids:
            return {}
        for _ in range(max(0, count)):
            target = random.choice(node_ids)
            self.nodes[target].load += 1
            self.nodes[target].version += 1
            self.nodes[target].snapshot()
        return {node_id: n.load for node_id, n in self.nodes.items()}

    def _run_wave_phase(self, rounds: int | None = None) -> None:
        if not self.nodes:
            return
        # Для связного направленного графа этого обычно достаточно для распространения знаний.
        total_rounds = rounds if rounds is not None else max(1, len(self.nodes) * 2)

        for node in self.nodes.values():
            node.snapshot()
            node.in_wave.clear()

        for _ in range(total_rounds):
            deliveries: Dict[str, List[WaveMessage]] = {node_id: [] for node_id in self.nodes}
            for src, out_neighbors in self.topology.items():
                src_state = self.nodes[src]
                msg = WaveMessage(sender=src, payload=dict(src_state.knowledge))
                for dst in out_neighbors:
                    deliveries[dst].append(msg)

            changed_any = False
            for dst, msgs in deliveries.items():
                dst_state = self.nodes[dst]
                for msg in msgs:
                    for known_node, value in msg.payload.items():
                        cur = dst_state.knowledge.get(known_node)
                        if cur is None or value[1] > cur[1]:
                            dst_state.knowledge[known_node] = value
                            changed_any = True
            if not changed_any:
                break

    def _run_transfer_phase(self) -> int:
        if not self.nodes:
            return 0

        known_loads_global = {
            node_id: node.knowledge.get(node_id, (node.load, node.version))[0]
            for node_id, node in self.nodes.items()
        }
        average = sum(known_loads_global.values()) / max(1, len(known_loads_global))
        planned_moves: List[Tuple[str, str, int]] = []

        for src, out_neighbors in self.topology.items():
            if not out_neighbors:
                continue
            src_state = self.nodes[src]
            src_estimated = src_state.knowledge.get(src, (src_state.load, src_state.version))[0]
            # Дискретная парная балансировка по дугам: переносим, если src заметно
            # перегружен относительно конкретного соседа (разница >= 2).
            candidates: List[Tuple[str, int]] = []
            for dst in out_neighbors:
                dst_state = self.nodes[dst]
                dst_estimated = src_state.knowledge.get(dst, (dst_state.load, dst_state.version))[0]
                diff = src_estimated - dst_estimated
                if diff >= 2:
                    candidates.append((dst, diff // 2))

            if not candidates:
                continue

            # Не "обнуляем" избыток в ноль из-за округления среднего:
            # держим минимум floor(avg), остальное можно отдавать.
            budget = max(0, src_state.load - int(average))
            if budget == 0:
                continue

            total_need = sum(need for _, need in candidates)
            budget = min(budget, total_need)
            allocated = 0
            for i, (dst, need) in enumerate(candidates):
                if i == len(candidates) - 1:
                    share = budget - allocated
                else:
                    share = int(round(budget * (need / max(1, total_need))))
                    share = min(share, budget - allocated)
                if share > 0:
                    planned_moves.append((src, dst, share))
                    allocated += share
                if allocated >= budget:
                    break

        total_moved = 0
        for src, dst, amount in planned_moves:
            if amount <= 0:
                continue
            src_state = self.nodes[src]
            dst_state = self.nodes[dst]
            actual = min(amount, src_state.load)
            if actual <= 0:
                continue
            src_state.load -= actual
            dst_state.load += actual
            src_state.version += 1
            dst_state.version += 1
            src_state.snapshot()
            dst_state.snapshot()
            total_moved += actual
        return total_moved

    def balance_step(self) -> Dict[str, Any]:
        before = {node_id: n.load for node_id, n in self.nodes.items()}
        self._run_wave_phase()
        moved = self._run_transfer_phase()
        after = {node_id: n.load for node_id, n in self.nodes.items()}
        return {
            "phase": str(uuid.uuid4())[:8],
            "before": before,
            "after": after,
            "moved_total": moved,
        }

    def balance_until_stable(self, max_steps: int = 20) -> Dict[str, Any]:
        history: List[Dict[str, Any]] = []
        for _ in range(max(1, max_steps)):
            step = self.balance_step()
            history.append(step)
            if step["moved_total"] == 0:
                break
        return {
            "steps": history,
            "final": {node_id: n.load for node_id, n in self.nodes.items()},
            "total_load": sum(n.load for n in self.nodes.values()),
        }
