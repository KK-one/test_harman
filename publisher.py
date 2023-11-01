import requests
import dataclasses
from task_queue import Task, Resources

url = "http://localhost:8080/queue"


task = Task(0,
            priority=2,
            resources=Resources(1,1,2), # Worker 1
            content='s3://path_content',
            result ='s3://path_result')

for i in range(10):
    task.id = i
    ans = requests.post(url, json=dataclasses.asdict(task))
    print(f'Send task_{task.id}, {ans}')

task.id+=1
task.priority = 0 # High priority
ans = requests.post(url, json=dataclasses.asdict(task))
print(f'Send task_{task.id}, {ans}. High priority')