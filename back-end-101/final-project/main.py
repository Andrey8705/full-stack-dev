from fastapi import FastAPI, HTTPException

app = FastAPI()

# Хранилище для задач в памяти
tasks = []
task_id_counter = 1  # Уникальный счетчик для ID задач


# Модель задачи (простая словарная структура)
def create_task(title: str, description: str):
    global task_id_counter
    task = {"id": task_id_counter, "title": title, "description": description}
    task_id_counter += 1
    return task


@app.get("/tasks/", summary="Получить список задач", description="Возвращает список всех задач.")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", summary="Получить задачу по ID", description="Возвращает задачу с указанным ID.")
def get_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks/", summary="Создать новую задачу", description="Добавляет новую задачу в список.")
def create_new_task(title: str, description: str):
    task = create_task(title, description)
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", summary="Обновить задачу", description="Обновляет данные существующей задачи.")
def update_task(task_id: int, title: str, description: str):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task["title"] = title
    task["description"] = description
    return task


@app.delete("/tasks/{task_id}", summary="Удалить задачу", description="Удаляет задачу с указанным ID.")
def delete_task(task_id: int):
    global tasks
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks = [t for t in tasks if t["id"] != task_id]
    return {"message": "Task deleted successfully"}
