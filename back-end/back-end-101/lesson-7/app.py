import argparse
import json
import os

TASKS_FILE = "tasks.json"

# Функция для загрузки задач из файла
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

# Функция для сохранения задач в файл
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Добавление задачи
def add_task(description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    tasks.append({"id": task_id, "description": description})
    save_tasks(tasks)
    print(f"Задача добавлена с ID {task_id}")

# Список задач
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Список задач пуст.")
        return
    for task in tasks:
        print(f"{task['id']}: {task['description']}")

# Обновление задачи
def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            save_tasks(tasks)
            print(f"Задача с ID {task_id} обновлена.")
            return
    print(f"Задача с ID {task_id} не найдена.")

# Удаление задачи
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Задача с ID {task_id} удалена.")

# Основная функция обработки аргументов
def main():
    parser = argparse.ArgumentParser(description="To-Do List Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Подкоманда add
    add_parser = subparsers.add_parser("add", help="Добавить новую задачу")
    add_parser.add_argument("description", type=str, help="Описание задачи")

    # Подкоманда list
    subparsers.add_parser("list", help="Показать список задач")

    # Подкоманда update
    update_parser = subparsers.add_parser("update", help="Обновить задачу")
    update_parser.add_argument("id", type=int, help="ID задачи")
    update_parser.add_argument("description", type=str, help="Новое описание задачи")

    # Подкоманда delete
    delete_parser = subparsers.add_parser("delete", help="Удалить задачу")
    delete_parser.add_argument("id", type=int, help="ID задачи")

    args = parser.parse_args()

    # Обработка команд
    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "delete":
        delete_task(args.id)

if __name__ == "__main__":
    main()
