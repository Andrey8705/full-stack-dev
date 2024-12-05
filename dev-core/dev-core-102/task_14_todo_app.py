import json
from datetime import datetime, date

# Функция для сохранения задач в файл
def save_tasks_to_file(tasks):
    for task in tasks:
        if 'due_date' in task and task['due_date']:
            task['due_date'] = task['due_date'].isoformat()  # Преобразуем дату в строку
        if 'subtasks' in task:
            for subtask in task['subtasks']:
                if 'due_date' in subtask and subtask['due_date']:
                    subtask['due_date'] = subtask['due_date'].isoformat()  # Преобразуем дату в строку
    
    try:
        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(tasks, file, indent=4)
        print("Задачи сохранены в файл.")
    except Exception as e:
        print(f"Ошибка при сохранении задач: {e}")

# Функция для загрузки задач из файла
def load_tasks_from_file():
    try:
        with open('tasks.json', 'r', encoding='utf-8') as file:
            tasks = json.load(file)
            for task in tasks:
                if 'due_date' in task and task['due_date']:
                    task['due_date'] = datetime.fromisoformat(task['due_date']).date()  # Преобразуем строку в дату
                if 'subtasks' in task:
                    for subtask in task['subtasks']:
                        if 'due_date' in subtask and subtask['due_date']:
                            subtask['due_date'] = datetime.fromisoformat(subtask['due_date']).date()  # Преобразуем строку в дату
            print("Задачи успешно загружены.")
            return tasks
    except Exception as e:
        print(f"Ошибка при загрузке задач: {e}")
        return []

# Функция для добавления задачи
def add_task(tasks, description, due_date_str):
    due_date = None
    if due_date_str:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()  # Преобразуем строку в дату
    task = {'description': description, 'completed': False, 'due_date': due_date, 'subtasks': []}
    tasks.append(task)
    tasks.sort(key=lambda x: x['due_date'] if x['due_date'] else date(9999, 12, 31))  # Сортировка по сроку
    print(f"Задача '{description}' добавлена.")

# Функция для добавления подзадачи
def add_subtask(tasks, task_index, description, due_date_str):
    if task_index < 0 or task_index >= len(tasks):
        print("Неверный номер задачи.")
        return
    
    due_date = None
    if due_date_str:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()  # Преобразуем строку в дату
    subtask = {'description': description, 'completed': False, 'due_date': due_date}
    tasks[task_index]['subtasks'].append(subtask)
    tasks[task_index]['subtasks'].sort(key=lambda x: x['due_date'] if x['due_date'] else date(9999, 12, 31))  # Сортировка подзадач по сроку
    print(f"Подзадача '{description}' добавлена к задаче '{tasks[task_index]['description']}'.")

# Функция для отображения всех задач
def view_tasks(tasks):
    if not tasks:
        print("Нет задач.")
    for idx, task in enumerate(tasks, 1):
        print(f"{idx}. {task['description']} — {'Выполнено' if task['completed'] else 'Не выполнено'}, срок: {task['due_date']}")
        for subtask_idx, subtask in enumerate(task['subtasks'], 1):
            print(f"  {subtask_idx}. Подзадача: {subtask['description']} — {'Выполнено' if subtask['completed'] else 'Не выполнено'}, срок: {subtask['due_date']}")

# Функция для пометки задачи как выполненной
def mark_task_completed(tasks, index):
    if index < 0 or index >= len(tasks):
        print("Задача не найдена.")
        return
    tasks[index]['completed'] = True
    print(f"Задача '{tasks[index]['description']}' помечена как выполненная.")

# Функция для пометки подзадачи как выполненной
def mark_subtask_completed(tasks, task_index, subtask_index):
    if task_index < 0 or task_index >= len(tasks):
        print("Задача не найдена.")
        return
    if subtask_index < 0 or subtask_index >= len(tasks[task_index]['subtasks']):
        print("Подзадача не найдена.")
        return
    tasks[task_index]['subtasks'][subtask_index]['completed'] = True
    print(f"Подзадача '{tasks[task_index]['subtasks'][subtask_index]['description']}' помечена как выполненная.")

# Функция для удаления задачи
def remove_task(tasks, index):
    if index < 0 or index >= len(tasks):
        print("Задача не найдена.")
        return
    removed_task = tasks.pop(index)
    print(f"Задача '{removed_task['description']}' удалена.")

# Главная функция
def main():
    tasks = load_tasks_from_file()  # Загружаем задачи из файла (если есть)
    while True:
        print("\nКоманды:")
        print("add — добавить новую задачу.")
        print("remove — удалить задачу.")
        print("view — показать все задачи.")
        print("complete — пометить задачу как выполненную.")
        print("subtask_add — добавить подзадачу.")
        print("subtask_complete — пометить подзадачу как выполненную.")
        print("exit — завершить выполнение программы.")
        command = input("Введите команду: ").strip().lower()
        
        if command == 'add':
            description = input("Введите описание задачи: ").strip()
            due_date_str = input("Введите срок выполнения (формат YYYY-MM-DD) или оставьте пустым: ").strip()
            add_task(tasks, description, due_date_str)
        
        elif command == 'remove':
            view_tasks(tasks)
            index = int(input("Введите номер задачи для удаления: ")) - 1
            remove_task(tasks, index)
        
        elif command == 'view':
            view_tasks(tasks)
        
        elif command == 'complete':
            view_tasks(tasks)
            index = int(input("Введите номер задачи для пометки как выполненной: ")) - 1
            mark_task_completed(tasks, index)
        
        elif command == 'subtask_add':
            view_tasks(tasks)
            task_index = int(input("Введите номер задачи для добавления подзадачи: ")) - 1
            description = input("Введите описание подзадачи: ").strip()
            due_date_str = input("Введите срок выполнения подзадачи (формат YYYY-MM-DD) или оставьте пустым: ").strip()
            add_subtask(tasks, task_index, description, due_date_str)
        
        elif command == 'subtask_complete':
            view_tasks(tasks)
            task_index = int(input("Введите номер задачи: ")) - 1
            subtask_index = int(input("Введите номер подзадачи: ")) - 1
            mark_subtask_completed(tasks, task_index, subtask_index)
        
        elif command == 'exit':
            save_tasks_to_file(tasks)  # Сохраняем задачи перед выходом
            print("Программа завершена.")
            break

        else:
            print("Неизвестная команда.")

# Запуск программы
if __name__ == "__main__":
    main()
