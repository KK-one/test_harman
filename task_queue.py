from dataclasses import dataclass
import asyncio
from functools import total_ordering
from asyncio import PriorityQueue

@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int


@dataclass
@total_ordering
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.id == other.id
        return False
    
    def __lt__(self, other):
        if isinstance(other, Task):
            return self.id < other.id
        return False

@dataclass
class Worker:
    id: int
    resources: Resources
    TIMEOUT: int = 10

class TaskQueue:
    queues = {}
    QUEUE_SIZE = 1_000

    async def init_resource_queue(self, resources: Resources) -> None:
        queue_id = self.resource2queue(resources)
        self.queues[queue_id] = PriorityQueue(self.QUEUE_SIZE)

    async def add_task(self, task: Task) -> None:
        queue_id = self.resource2queue(task.resources)
        if queue_id not in self.queues:
            await self.init_resource_queue(task.resources)
        await self.queues[queue_id].put((task.priority, task))
        return f"Task_{task.id} added"

    async def get_task(self, resources: Resources) -> Task:
        queue_id = self.resource2queue(resources)
        if queue_id in self.queues:
            task = await self.queues[queue_id].get()
            self.queues[queue_id].task_done()
        return task

    def resource2queue(self, resources: Resources) -> str:
        return f"{resources.ram}_{resources.cpu_cores}_{resources.gpu_count}"