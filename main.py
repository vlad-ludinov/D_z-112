import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# pip install fastapi


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str


class TaskIn(BaseModel):
    title: str
    description: str
    status: str


tasks = []


@app.get("/tasks/", response_model=list[Task])
async def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task_by_id(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task


@app.post("/tasks/", response_model=Task)
async def create_task(new_task: TaskIn):
    if not tasks:
        tasks.append(
            Task(
                id=1,
                title=new_task.title,
                description=new_task.description,
                status=new_task.status,
            )
        )
        return tasks[-1]
    else:
        tasks.append(
            Task(
                id=tasks[-1].id + 1,
                title=new_task.title,
                description=new_task.description,
                status=new_task.status,
            )
        )
        return tasks[-1]


@app.put("/tasks/{task_id}", response_model=Task)
async def edit_task(task_id: int, new_task: TaskIn):
    index = 0
    for task in tasks:
        if task.id == task_id:
            tasks[index] = Task(
                id=task_id,
                title=new_task.title,
                description=new_task.description,
                status=new_task.status,
            )
            return tasks[index]
        index += 1


@app.delete("/tasks/{task_id}", response_model=Task)
async def get_task_by_id(task_id: int):
    index = 0
    for task in tasks:
        if task.id == task_id:
            removed_task = tasks.pop(index)
            return removed_task
        index += 1


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
