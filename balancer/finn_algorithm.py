from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple
from balancer.config import TREE


@dataclass
class FinnMessage:

    sender: str
    inc: Set[str]
    ninc: Set[str]


@dataclass
class FinnProcess:

    pid: str
    incoming: List[str]
    outgoing: List[str]
    inc: Set[str] = field(default_factory=set)
    ninc: Set[str] = field(default_factory=set)
    inbox: List[FinnMessage] = field(default_factory=list)

    def initialize(self) -> List[FinnMessage]:
        """
        Начальная инициализация:
        Inc(s) = {s}, NInc(s) = пусто.
        Рассылаем первое сообщение всем соседям по выходу.
        """
        self.inc = {self.pid}
        self.ninc = set()
        return self._broadcast_if_changed(previous_inc=set(), previous_ninc=set())

    def _broadcast_if_changed(
        self, previous_inc: Set[str], previous_ninc: Set[str]
    ) -> List[FinnMessage]:

        if self.inc == previous_inc and self.ninc == previous_ninc:
            return []

        msg = FinnMessage(sender=self.pid, inc=set(self.inc), ninc=set(self.ninc))
        return [FinnMessage(sender=msg.sender, inc=msg.inc, ninc=msg.ninc)] * len(
            self.outgoing
        )

    def process_round(self) -> Tuple[List[Tuple[str, FinnMessage]], bool]:
        if not self.inbox:
            return [], False

        prev_inc = set(self.inc)
        prev_ninc = set(self.ninc)

        # Все отправители из этого раунда
        senders_this_round: Set[str] = set()

        while self.inbox:
            msg = self.inbox.pop(0)
            senders_this_round.add(msg.sender)
            self.inc |= msg.inc
            self.ninc |= msg.ninc

        # Если получили сообщения от всех соседей по входу, включаем себя в NInc
        if set(self.incoming).issubset(senders_this_round):
            self.ninc.add(self.pid)

        # Рассылаем сообщения, если множества изменились
        out_messages: List[Tuple[str, FinnMessage]] = []
        if self.inc != prev_inc or self.ninc != prev_ninc:
            msg_template = FinnMessage(sender=self.pid, inc=set(self.inc), ninc=set(self.ninc))
            for neighbor in self.outgoing:
                out_messages.append(
                    (neighbor, FinnMessage(sender=msg_template.sender,
                                           inc=set(msg_template.inc),
                                           ninc=set(msg_template.ninc)))
                )

        changed = (self.inc != prev_inc) or (self.ninc != prev_ninc)
        return out_messages, changed


def build_processes_from_tree() -> Dict[str, FinnProcess]:
    incoming: Dict[str, List[str]] = {node_id: [] for node_id in TREE.keys()}
    outgoing: Dict[str, List[str]] = {node_id: [] for node_id in TREE.keys()}

    for node_id, info in TREE.items():
        children = info.get("children", [])
        outgoing[node_id] = list(children)
        for child in children:
            incoming.setdefault(child, []).append(node_id)

    processes: Dict[str, FinnProcess] = {}
    for node_id in TREE.keys():
        processes[node_id] = FinnProcess(
            pid=node_id,
            incoming=incoming.get(node_id, []),
            outgoing=outgoing.get(node_id, []),
        )
    return processes


def run_finn_algorithm(initiator: str = "master", max_rounds: int = 100) -> Dict[str, Dict[str, Set[str]]]:
    processes = build_processes_from_tree()
    if initiator not in processes:
        raise ValueError(f"Unknown initiator: {initiator}")

    # Начальная инициализация: только инициатор запускает рассылку
    initial_msgs = processes[initiator].initialize()
    for neighbor, msg in zip(processes[initiator].outgoing, initial_msgs):
        processes[neighbor].inbox.append(msg)

    for _round in range(max_rounds):
        any_changed = False
        pending_sends: List[Tuple[str, str, FinnMessage]] = []

        # Каждый узел обрабатывает свои входящие сообщения этого раунда
        for pid, proc in processes.items():
            sends, changed = proc.process_round()
            any_changed = any_changed or changed
            for receiver, msg in sends:
                pending_sends.append((pid, receiver, msg))

        # Рассылаем сообщения следующего раунда
        for _sender, receiver, msg in pending_sends:
            processes[receiver].inbox.append(msg)

        # Проверяем условие завершения: во всей сети Inc == NInc и больше нет изменений
        if any_changed:
            continue

        all_equal = all(proc.inc == proc.ninc for proc in processes.values())
        if all_equal:
            break

    # Формируем результат
    result: Dict[str, Dict[str, Set[str]]] = {}
    for pid, proc in processes.items():
        result[pid] = {"Inc": set(proc.inc), "NInc": set(proc.ninc)}
    return result


def demo_finn() -> None:
    result = run_finn_algorithm("master")
    print("Результат работы алгоритма Финна:")
    for pid in sorted(result.keys()):
        inc = ", ".join(sorted(result[pid]["Inc"]))
        ninc = ", ".join(sorted(result[pid]["NInc"]))
        print(f"{pid}:")
        print(f"  Inc  = {{{inc}}}")
        print(f"  NInc = {{{ninc}}}")


if __name__ == "__main__":
    demo_finn()

