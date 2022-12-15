from fastapi import Body, FastAPI, Request
from fastapi.responses import JSONResponse

from celery.result import AsyncResult
from worker.tasks import some_task

app = FastAPI()


@app.get("/ping")
def ping():
    return {"ping": "pong"}


@app.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    # task_type = payload["type"]
    task = some_task.delay()
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
