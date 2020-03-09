from app import scaler_helpers, load_balancer
class CloudMonitor:
    def __init__(self, pool):
        self._pool = pool
        self._api = scaler_helpers.get_api()
    
    def get_cpu_utilization_for_registered_instances(self):

        instances_data_points = {}
        for instance_id in self._pool.get_registered_instances_ids():
            instances_data_points[instance_id] =  self._api.get_average_cpu_utilization(
                [{'Name': 'InstanceId', 'Value': instance_id }])['Datapoints']

        return instances_data_points

    def get_http_request_rate_for_registered_instances(self):
    #To be implemented#
            return
    
cloud_monitor = CloudMonitor(load_balancer.get_load_balancer())
def get_cloud_monitor():
    return cloud_monitor