import pytest
from task_queue import TaskQueue, Task, Resources


class TestResources:
    #ToDo: Move Resources and Task to Publisher 
    def test_default_resources(self):
        r1 = Resources()
        r2 = Resources(None, None, None)
        assert r1==r2

    def test_unlim_ram(self):
        with pytest.raises(ValueError):
            res = Resources(Resources.RAM_LIM+1, 1, 1)

    def test_unlim_cpu(self):
        with pytest.raises(ValueError):
            res = Resources(1, Resources.CPU_LIM+1, 1)

    def test_unlim_gpu(self):
        with pytest.raises(ValueError):
            res = Resources(1, 1, Resources.GPU_LIM+1)

    def test_zero_ram(self):
        with pytest.raises(ValueError):
            res = Resources(0, 1, 1)

    def test_zero_cpu(self):
        with pytest.raises(ValueError):
            res = Resources(1, 0, 1)

    def test_zero_gpu(self):
        with pytest.raises(ValueError):
            res = Resources(1, 1, 0)

    def test_type_ram(self):
        with pytest.raises(TypeError):
            res = Resources("", 1, 1)

    def test_type_cpu(self):
        with pytest.raises(TypeError):
            res = Resources(1, "", 1)

    def test_type_gpu(self):
        with pytest.raises(TypeError):
            res = Resources(1, 1, "")

    @pytest.mark.smoke
    def test_min_resources(self):
        r1 = Resources(1,1,1)
        assert (r1.ram, r1.cpu_cores, r1.gpu_count) == (1,1,1)


class TestTask():
    #ToDo: Check Publisher unittest task, Unique ID and etc.

    def test_type_resources(self):
        with pytest.raises(TypeError):
            task = Task(0, 0, [], "s3://content","s3://result")

    @pytest.mark.smoke
    def test_min_task(self, resource):
        task = Task(0, 0, resource, "s3://content", "s3://result")
        assert task.id == 0
        assert task.priority == 0
        assert task.resources == resource
        assert task.content == "s3://content"
        assert task.result == "s3://result"


@pytest.fixture
def resources():
    return  Resources(1,1,1)

@pytest.fixture
def task(resources):
    return Task(0, 0, resources ,"s3://content","s3://result")

@pytest.fixture
def task2(task):
    task.id +=1
    return task

@pytest.fixture
def queue():
    return TaskQueue()

class TestQueue:
    def test_empty_queue(self, queue, resources):
        assert queue.get_task(resources) is None

    def test_add_empty_task(self, queue):
        with pytest.raises(TypeError):
            queue.add_task()

    def test_get_empty_task(self, queue):
        with pytest.raises(TypeError):
            queue.get_task()

    @pytest.mark.smoke
    def test_add_task(self, queue, task):
        queue.add_task(task)
        print()
        print(task)
        print()
        assert task in queue

    @pytest.mark.smoke
    def test_get_task(self, queue, task):
        assert task.id == queue.get_task(task.resources).id

    @pytest.mark.smoke
    def test_queue_has_1_task(self, queue, task):
        queue.add_task(task)
        assert queue.get_task(task.resources).id == task.id

    def test_task_free_queue(self, queue, task):
        queue.add_task(task)
        queue.get_task(task.resources)
        # ToDo: Check queue has special empty status
        assert task not in queue

    def test_correct_task_priority(self, queue, task, task2):
        task.priority += 1
        queue.add_task(task)
        queue.add_task(task2)
        return_task = queue.get_task(task.resources)
        assert task.id == return_task.id
        assert task.priority == return_task.priority

    def test_correct_resource_task(self, queue, task, task2):
        task2.resources.gpu_count += 1
        queue.add_task(task)
        queue.add_task(task2)
        return_task = queue.get_task(task.resources)
        assert task.id == return_task.id
        assert task.resources == return_task.resources

    def test_correct_earlier_task(self, queue, task, task2):
        queue.add_task(task)
        queue.add_task(task2)
        return_task = queue.get_task(task.resources)
        assert task.id == return_task.id

    def test_save_after_err(self, queue, task, task2):
        queue.add_task(task)
        queue.add_task(task2)
        queue.get_task(task.resources)
        dump = queue.__del__()
        queue_restore = dump.read()
        assert dump.exists()
        assert task2 in queue_restore
        assert task not in queue_restore

    # ToDo: Stress test for 1_000> num get/set requests
    # ToDo: Integration test Publisher->Queue: 1) set_correct_task
    # 2) test_stress_num_task 3) test_
    # ToDo: Integration test Queue->Consumer:  1) get_correct_task
    # 2) test_priority_task 3) test_uncostrain_resourse_task
