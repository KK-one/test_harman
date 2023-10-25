from dataclasses import dataclass

@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int
    RAM_LIM: int = 32
    CPU_LIM: int = 8
    GPU_LIM: int = 8

@dataclass
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str


class TaskQueue:
    def add_task(self, task: Task) -> None:
        pass

    def get_task(self, available_resources: Resources) -> Task:
        pass
