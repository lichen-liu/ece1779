from app import pool_monitor_helper
import datetime
import thread
class AutoScaler:
    def __init__(self, pool_monitor_helper, pool):
        self._max_threshold = 0.8
        self._min_threshold = 0.5
        self._growing_ratio = 1.5
        self._shrinking_ratio = 0.5
	self._pool_monitor_helper = pool_monitor_helper
	self._pool = pool
	self._operation_timestamp = datetime.time(0, 0)
	self._minimum_operation_cooldown = datetime.timedelta(seconds = 10) 

    def set_max_threshold(self, threshold):
        self._max_threshold = threshold
    
    def set_min_threshold(self, threshold):
        self._min_threshold = threshold

    def set_growing_ratio(self, ratio):
        self._growing_ratio = ratio
    
    def set_shrinking_ratio(self, ratio):
        self._shrinking_ratio = ratio

    def get_max_threshold(self):
        return self._max_threshold 
    
    def get_min_threshold(self):
        return self._min_threshold 

    def get_growing_ratio(self):
        return self._growing_ratio 
    
    def get_shrinking_ratio(self):
        return self._shrinking_ratio 
    def start(self):

    def auto_scaling(self):
	average = self.monitor_average_pool_cpu_usage()
	if average > self._max_threshold:
	    try_increase_pool_size()
	if average < self._min_threshold:
	    try_decrease_pool_size()
	

    def monitor_average_work_pool_cpu_usage(self):
	current_instance_utilizations = self._pool_monitor_helper.get_current_cpu_utilization_for_registered_instances()
	utilization_addition = 0
	instance_number = 0
	for instance_id in current_instance_utilizations:
            utilization_addition += current_instance_utilization[instance_id]
	    instance_number += 1
	return utilization_addition / instance_number
 	 
    def try_increase_pool_size(self):
	if is_cooldown_finished:
	    worker_count = self._pool_monitor_helper.get_number_of_running_workers_in_pool()
	    required_count = ceil(worker_count * self._growing_ratio)
	    self._pool.increase_pool_by_size(required_count - worker_count)
	    self._operation_timestamp = datetime.now()
    def try_decrease_pool_size(self):    
	if is_cooldown_finished:
            worker_count = self._pool_monitor_helper.get_number_of_running_workers_in_pool()
	    if worker_count <= self._pool.get_minimum_work:
		return
            required_count = ceil(worker_count * self._shrinking_ratio)
            self._pool.decrease_pool_by_size(required_count - worker_count)
            self._operation_timestamp = datetime.now()


auto_scaler = AutoScaler()
def get_auto_scaler():
    return auto_scaler
