
# Task

```
Task description:
* Requires a task queue with priorities and resource limits.
* Each task has a priority and the required amount of resources to process it.
* Publishers create tasks with specified resource limits, and put them in a task queue.
* Consumer receives the highest priority task that satisfies available resources.
* The queue is expected to contain thousands of tasks.
* Write a unit test to demonstrate the operation of the queue.
```

# Initial code

```python
from dataclasses import dataclass

@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int


@dataclass
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str


class TaskQueue:
    def add_task(self):
        pass

    def get_task(self, available_resources: Resources) -> Task:
        pass
```

# Run Tets

Smoke test - check failure of basic functions
```shell
pytest -m "smoke" test_queue.py
```
Run unit tests
```shell
pytest  test_queue.py
``` 

