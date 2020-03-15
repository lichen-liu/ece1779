from manager_app import pool_monitor_helper, ec2_pool
from datetime import datetime, timedelta
import threading
import math
import time


class AutoScaler:
    def __init__(self, pool_monitor_helper, pool):
        self._max_threshold = 0.6
        self._min_threshold = 0.1
        self._growing_ratio = 1.5
        self._shrinking_ratio = 0.5
        self._pool_monitor_helper = pool_monitor_helper
        self._pool = pool
        self._operation_timestamp = datetime(1970, 1, 1, 0, 0)
        # Allow resizing operation to take up to 2 mins 
        self._resizing_timeout = timedelta(seconds = 150) 
        self._next_pool_size = 0
        self._cooldown_period = timedelta(seconds = 90)
        self._monitoring_interval = 10
        self._running_thread = threading.Thread(
            target=self.auto_scaling, daemon=True)
        self._started = False

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
        if not self._started:
            self._started = True
            self._running_thread.start()

    def auto_scaling(self):
        # averages = [0]
        while True:
            if(self._is_operation_finished_or_timeout()):
                average = self.calculate_average_work_pool_cpu_usage() / 100
                # averages.append(average)
                # # Only track the last two minutes CPU utilization
                # if len(averages) > 2:
                #     averages = averages[1:]
                # if (averages[0] + averages[1]) / 2.0 > self._max_threshold:
                #     self.try_increase_pool_size()
                # if (averages[0] + averages[1]) / 2.0 < self._min_threshold:
                #     self.try_decrease_pool_size()
                if average > self._max_threshold:
                    self.try_increase_pool_size()
                if average < self._min_threshold:
                    self.try_decrease_pool_size()
                time.sleep(self._monitoring_interval)

    def calculate_average_work_pool_cpu_usage(self):
        current_instance_utilizations = self._pool_monitor_helper.get_current_cpu_utilization_for_registered_instances()
        utilization_sum_up = 0
        instance_count = 0
        for instance_id in current_instance_utilizations:
            utilization_sum_up += current_instance_utilizations[instance_id]
            instance_count += 1

        if instance_count == 0:
            return 0

        return utilization_sum_up / instance_count

    def try_increase_pool_size(self):
        worker_count = self._pool_monitor_helper.get_number_of_running_workers_in_pool()
        upsized_count = math.ceil(worker_count * self._growing_ratio)

        self._pool.increase_pool_by_size(upsized_count - worker_count)
        self.update_timestamp()
        self._next_pool_size = upsized_count

    def try_decrease_pool_size(self):
        worker_count = self._pool_monitor_helper.get_number_of_running_workers_in_pool()
        min_required_worker = self._pool.get_min_worker_count()
        if worker_count <= min_required_worker:
            return

        downsized_count = math.floor(worker_count * self._shrinking_ratio)
        if(downsized_count < min_required_worker):
            downsized_count = min_required_worker

        self._pool.decrease_pool_by_size(worker_count - downsized_count)
        self.update_timestamp()
        self._next_pool_size = downsized_count

    def _is_operation_finished_or_timeout(self):
        if(self._operation_timestamp + self._resizing_timeout < datetime.now()):
            return True
        if(self._pool_monitor_helper.get_number_of_running_workers_in_pool() == self._next_pool_size):
            # This allows the incoming requests to be received by latest pool
            time.sleep(self._cooldown_period)
            return True
       
        return False

    def update_timestamp(self):
        self._operation_timestamp = datetime.now()


helper = pool_monitor_helper.get_monitor_helper()
pool = ec2_pool.get_worker_pool()
auto_scaler = AutoScaler(helper, pool)


def get_auto_scaler():
    return auto_scaler
