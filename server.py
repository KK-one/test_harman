import asyncio

from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from task_queue import Resources, Task, Worker, TaskQueue

app = Application()
routers = web.RouteTableDef()
QUEUE_KEY = 'QUEUE_KEY'
WORKER_KEY = 'WORKER_KEY'


async def process_worker(worker: Worker, queue: TaskQueue):
    while True:
        task = await queue.get_task(worker.resources)
        await asyncio.sleep(worker.TIMEOUT)
        print(f"Worker_{worker.id}, finished to process_{task}")


@routers.post("/queue")
async def add_task(request: Request) -> Response:
    queue = app[QUEUE_KEY]
    body = await request.json()
    task = Task(**body)
    task.resources = Resources(**body['resources'])
    print(f'App: Request task_{task.id}')
    resp = await queue.add_task(task)
    return Response(body=resp)

async def create_queue_workers(app: Application) -> None:
    WORKERS_NUM = 3
    print(f'App: Iniatialize TaskQueue and {WORKERS_NUM} workers')
    queue = TaskQueue()
    workers = []
    for i in range(WORKERS_NUM):
        worker = Worker(id=i, resources=Resources(1,1,i+1))
        await queue.init_resource_queue(worker.resources)
        workers.append(asyncio.create_task(process_worker(worker, queue)))
    app[QUEUE_KEY] = queue
    app[WORKER_KEY] = workers
    print(f'App: Initialize TaskQueue and workers succes')

async def destroy_queue_workers(app: Application) -> None:
    queue = app[QUEUE_KEY]
    workers = app[WORKER_KEY]
    TIMEOUT_JOBS = 10
    try:
        print(f"App: Wait for {TIMEOUT_JOBS}sec to let all tasks done.")
        await asyncio.wait_for(queue.join(), timeout=TIMEOUT_JOBS)
    except Exception as err:
        print(f'App: Cancel all workers')
        [task.cancel() for task in workers]


app.add_routes(routers)
app.on_startup.append(create_queue_workers)
app.on_shutdown.append(destroy_queue_workers)
web.run_app(app)