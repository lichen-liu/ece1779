import threading
from contextlib import contextmanager

class Task:
    def __init__(self, source_dir, thumbnail_dest_dir, rectangled_dest_dir):
        self.source_dir = source_dir
        self.thumbnail_dest_dir = thumbnail_dest_dir
        self.rectangled_dest_dir = rectangled_dest_dir

class Queue:
    def __init__(self, capacity):
        self._lock = threading.RLock()
        self._task_wait_condition = threading.Condition(self._lock)
        self._capacity = capacity
        self._queue = []
        self._lock_timeout = 5

    def has_task(self):
        return len(self._queue) > 0

    def is_full(self):
        return len(self._queue) >= self._capacity
    
    def wait_task(self):
        self._task_wait_condition.wait() 

    def notify_waiters(self):
        self._task_wait_condition.notifyAll()
    
    @contextmanager
    def acquire_lock(self, use_timeout = True):
        if use_timeout:
            result = self._lock.acquire(blocking=True, timeout=self._lock_timeout)
        else:
            result = self._lock.acquire(blocking=True)
        yield result
        if result:
            self._lock.release()

    def add(self, task):
        if(self.is_full()):
            return False
        self._queue.insert(0,task)
        self.notify_waiters()
        return True
            
    # The Consumer (batch_handler) will keep waiting to ...
    # ... get a task, if there is no test, the consumer sleeps on the condition
    def pop(self, needed = 1):
        tasks = []
        while(needed > 0 and self.has_task()):
            tasks.append(self._queue.pop())
            needed = needed - 1
        return tasks

capacity = 100
queue = Queue(capacity)
def get_queue():     
    return queue



    
   
    
    
    
   
  