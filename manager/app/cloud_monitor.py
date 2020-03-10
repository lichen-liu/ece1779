from user_app import scaler_helpers, load_balancer
class CloudMonitor:
    def __init__(self, pool):
        self._pool = pool
        self._api = scaler_helpers.get_api()
    
    def get_cpu_utilization_for_registered_instances(self):

        dimensions = []
        for instance_id in self._pool.get_registered_instances_ids():
            dimensions.append(
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                }
            )
        
        return self._api.get_average_cpu_utilization(dimensions)
    

cloud_monitor = CloudMonitor(load_balancer.get_load_balancer())
def get_cloud_monitor():
    return cloud_monitor