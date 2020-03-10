from datetime import datetime
from app import pool_monitor_helper
import threading, time
class WorkerCountMonitor:
    def __init__(self, helper):
        self._helper = helper
        self._running_thread = threading.Thread(target = self.start_monitor, daemon = True)
        self._worker_counts_record = []
        self._period = 60
        self._time_range = 1800
        self._record_max_count = self._time_range / self._period
        self._started = False
    
    def get_current_worker_count(self):
        return self._helper.get_number_of_running_workers_in_pool()
    
    def get_count_status(self):
        return self._worker_counts_record

    def insert_record(self):
        self._worker_counts_record.append({
            "Timestamp" : datetime.now().strftime("%H:%M"),
            "Count" : self.get_current_worker_count()
        })    
        if(len(self._worker_counts_record) > self._record_max_count):
            self._worker_counts_record.pop(0)
    
    def start_monitor(self):
        while True:
            self.insert_record()
            print(self._worker_counts_record)
            time.sleep(self._period)

    def start(self):
        self._started = True
        self._running_thread.start()

monitor = WorkerCountMonitor(pool_monitor_helper.get_monitor_helper())
def get_worker_count_monitor():
    return monitor



    


