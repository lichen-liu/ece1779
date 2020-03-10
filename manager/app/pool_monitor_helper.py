from app import aws_api_helper, ec2_pool
class PoolMonitoringHelper:
    def __init__(self, pool):
        self._pool = pool
        self._api = aws_api_helper.get_api()
    
    def get_cpu_utilization_for_registered_instances(self):

        instances_data_points = {}
        for instance_id in self._pool.get_registered_instances_ids():
            instances_data_points[instance_id] =  self._api.get_average_cpu_utilization(
                [{'Name': 'InstanceId', 'Value': instance_id }])['Datapoints']

        return instances_data_points

    def get_http_request_rate_for_registered_instances(self):
    #To be implemented#
            return
        
    def get_number_of_running_workers_in_pool(self):
        work_count = 0
        health_status = self._pool.get_registered_instances_health_status()
        for instance_id in health_status:
            if(health_status[instance_id] == 'healthy'):
                work_count += 1
        return work_count

    
helper = PoolMonitoringHelper(ec2_pool.get_worker_pool())
def get_monitor_helper():
    return helper