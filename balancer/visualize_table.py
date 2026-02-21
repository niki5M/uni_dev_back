#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерация визуализации дерева с нагрузками в виде таблицы (HTML).
Скрипт запрашивает данные у мастера и создаёт HTML-файл с таблицей.
Запускать из корня проекта: back_uni/
"""
import httpx
import sys
import os
from datetime import datetime

# Добавить корень проекта в путь для импорта (работает из любой директории)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from balancer.config import TREE, get_all_workers

MASTER_URL = "http://127.0.0.1:9000"


def get_loads():
    """Получить нагрузки от мастера."""
    try:
        with httpx.Client(timeout=3.0) as client:
            r = client.get(f"{MASTER_URL}/loads")
            if r.status_code != 200:
                print(f"Ошибка получения нагрузок: {r.status_code}")
                return {}
            return r.json()
    except httpx.ConnectError:
        print(f"❌ Не удалось подключиться к мастеру на {MASTER_URL}")
        print("   Убедитесь, что мастер запущен: python3 -m uvicorn balancer.master:app --host 0.0.0.0 --port 9000")
        return {}
    except Exception as e:
        print(f"Ошибка: {e}")
        return {}


def build_tree_table(loads: dict) -> str:
    """Построить HTML-таблицу дерева с нагрузками."""
    html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Визуализация балансировки нагрузки</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .timestamp {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        th {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .node-master {
            background-color: #e3f2fd;
            font-weight: bold;
        }
        .node-group {
            background-color: #fff3e0;
        }
        .node-worker {
            background-color: #f1f8e9;
        }
        .load-high {
            color: #d32f2f;
            font-weight: bold;
        }
        .load-medium {
            color: #f57c00;
        }
        .load-low {
            color: #388e3c;
        }
        .load-unavailable {
            color: #999;
            font-style: italic;
        }
        .tree-structure {
            font-family: monospace;
            white-space: pre;
            background-color: #f9f9f9;
            padding: 15px;
            border: 1px solid #ddd;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>Визуализация балансировки нагрузки</h1>
    <div class="timestamp">Время: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</div>
    
    <h2>Дерево узлов</h2>
    <div class="tree-structure">"""
    
    def build_tree_text(node_id: str, prefix: str = "", is_last: bool = True) -> str:
        """Рекурсивно строит текстовое дерево."""
        node_info = TREE[node_id]
        load = loads.get(node_id, -1)
        load_str = f" (нагрузка: {load})" if load >= 0 else " (недоступен)"
        marker = "└── " if is_last else "├── "
        result = f"{prefix}{marker}{node_id}{load_str}\n"
        
        children = node_info["children"]
        if children:
            new_prefix = prefix + ("    " if is_last else "│   ")
            for i, child_id in enumerate(children):
                is_last_child = (i == len(children) - 1)
                result += build_tree_text(child_id, new_prefix, is_last_child)
        return result
    
    tree_text = "master (инициатор)\n"
    for i, child_id in enumerate(TREE["master"]["children"]):
        is_last = (i == len(TREE["master"]["children"]) - 1)
        tree_text += build_tree_text(child_id, "", is_last)
    
    html += tree_text + """
    </div>
    
    <h2>Таблица нагрузок</h2>
    <table>
        <thead>
            <tr>
                <th>ID узла</th>
                <th>Тип</th>
                <th>Порт</th>
                <th>Родитель</th>
                <th>Дети</th>
                <th>Нагрузка</th>
                <th>Статус</th>
            </tr>
        </thead>
        <tbody>"""
    
    # Сортируем узлы: master, затем groups, затем workers
    nodes_order = ["master"] + \
                  [n for n, info in TREE.items() if info.get("type") == "intermediate"] + \
                  [n for n, info in TREE.items() if info.get("type") == "leaf"]
    
    for node_id in nodes_order:
        node_info = TREE[node_id]
        load = loads.get(node_id, -1)
        node_type = node_info.get("type", "unknown")
        port = node_info.get("port", "?")
        parent = node_info.get("parent", "-")
        children = ", ".join(node_info.get("children", [])) or "-"
        
        # CSS классы
        row_class = ""
        if node_type == "initiator":
            row_class = "node-master"
        elif node_type == "intermediate":
            row_class = "node-group"
        elif node_type == "leaf":
            row_class = "node-worker"
        
        # Класс для нагрузки
        load_class = ""
        if load == -1:
            load_class = "load-unavailable"
            load_display = "недоступен"
            status = "❌ Недоступен"
        elif load >= 7:
            load_class = "load-high"
            load_display = str(load)
            status = "🔴 Высокая"
        elif load >= 3:
            load_class = "load-medium"
            load_display = str(load)
            status = "🟡 Средняя"
        else:
            load_class = "load-low"
            load_display = str(load)
            status = "🟢 Низкая"
        
        html += f"""
            <tr class="{row_class}">
                <td><strong>{node_id}</strong></td>
                <td>{node_type}</td>
                <td>{port}</td>
                <td>{parent}</td>
                <td>{children}</td>
                <td class="{load_class}">{load_display}</td>
                <td>{status}</td>
            </tr>"""
    
    html += """
        </tbody>
    </table>
    
    <h2>Статистика</h2>
    <table>
        <thead>
            <tr>
                <th>Метрика</th>
                <th>Значение</th>
            </tr>
        </thead>
        <tbody>"""
    
    workers = get_all_workers()
    worker_loads = {w: loads.get(w, -1) for w in workers if loads.get(w, -1) >= 0}
    if worker_loads:
        total_load = sum(worker_loads.values())
        avg_load = total_load / len(worker_loads) if worker_loads else 0
        max_load = max(worker_loads.values()) if worker_loads else 0
        min_load = min(worker_loads.values()) if worker_loads else 0
        
        html += f"""
            <tr>
                <td>Всего воркеров</td>
                <td>{len(workers)}</td>
            </tr>
            <tr>
                <td>Доступных воркеров</td>
                <td>{len(worker_loads)}</td>
            </tr>
            <tr>
                <td>Общая нагрузка</td>
                <td>{total_load}</td>
            </tr>
            <tr>
                <td>Средняя нагрузка</td>
                <td>{avg_load:.2f}</td>
            </tr>
            <tr>
                <td>Максимальная нагрузка</td>
                <td>{max_load}</td>
            </tr>
            <tr>
                <td>Минимальная нагрузка</td>
                <td>{min_load}</td>
            </tr>
            <tr>
                <td>Разница (max - min)</td>
                <td>{max_load - min_load}</td>
            </tr>"""
    
    html += """
        </tbody>
    </table>
</body>
</html>"""
    return html


def main():
    """Генерация HTML-файла с визуализацией."""
    import os
    
    # Определить имя файла: если указан аргумент "до" или "после", добавить суффикс
    suffix = ""
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ["до", "before", "pre"]:
            suffix = "_до_балансировки"
        elif sys.argv[1].lower() in ["после", "after", "post"]:
            suffix = "_после_балансировки"
        else:
            suffix = f"_{sys.argv[1]}"
    
    output_file = f"balancer_visualization{suffix}.html"
    
    print("Получение данных от мастера...")
    loads = get_loads()
    
    if not loads:
        print("Не удалось получить данные. Убедитесь, что мастер запущен на порту 9000.")
        return
    
    print("Генерация таблицы...")
    html = build_tree_table(loads)
    
    # Сохранить в папку balancer или текущую директорию
    filepath = os.path.join("balancer", output_file) if os.path.exists("balancer") else output_file
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Визуализация сохранена в файл: {filepath}")
    print(f"Откройте файл в браузере для просмотра.")
    print(f"\nИспользование:")
    print(f"  python3 balancer/visualize_table.py до    # создать файл 'до балансировки'")
    print(f"  python3 balancer/visualize_table.py после # создать файл 'после балансировки'")


if __name__ == "__main__":
    main()
