from manager_app import aws_api_helper, manager_config
class EC2Pool:
    def __init__(self):
        self._default_load_balancer_index = 0
        self._default_target_group_index = 0
        self._api = aws_api_helper.get_api()
        self._load_balancer_arn = self.init_default_load_balancer()
        self._target_group_arn = self.init_default_target_group()
        self._min_work_count = 1
        self._defined_working_status = {'healthy', 'unhealthy'}
        self._hosting_ec2_id = manager_config.get_hosting_ec2_id() 
    def init_default_load_balancer(self):
        load_balancers = self._api.get_load_balancers()
        return load_balancers['LoadBalancers'][self._default_load_balancer_index]['LoadBalancerArn']
    
    def init_default_target_group(self):
        target_groups = self._api.get_target_group_on_load_balancer(self._load_balancer_arn)
        return target_groups['TargetGroups'][self._default_target_group_index]['TargetGroupArn']

    def get_working_status(self):
        return self._defined_working_status

    def get_min_worker_count(self):
        return self._min_work_count
    
    def get_all_running_instances_ids(self):
        instances = self._api.get_running_ec2_instance()
        print(instances)
        for instance in instances:
            print(instance)
        return [ {'Id' : str(instance.id)} for instance in instances]

    def get_registered_instances_health_status(self):
        targets_status = self._api.get_health_status_on_group_targets(self._target_group_arn)
        instances_health_status = {}
        for target in targets_status['TargetHealthDescriptions']:
            instances_health_status[target['Target']['Id']] = target['TargetHealth']['State']

        return instances_health_status 
    
    def stop_all_registerd_instaces(self):
        registered_ids = self.get_registered_instances_ids()
        self._api.shutdown_ec2_instances_by_ids()

    def get_registered_instances_ids(self):
        return self.get_registered_instances_health_status().keys()

    def get_available_ec2_instance_ids(self):
        all_running_ids = self.get_all_running_instances_ids()
        registered_ids = self.get_registered_instances_ids()
        available_ec2_ids = []
        for running_id in all_running_ids:
            if running_id['Id'] not in registered_ids and running_id['Id'] != self._hosting_ec2_id:
                available_ec2_ids.append(running_id)
        return available_ec2_ids

    def increase_pool_by_size(self, num = 1):
        target_ids = []
        available_ids = self.get_available_ec2_instance_ids()

        for available_id in available_ids:
            if(num <= 0):
                break
            target_ids.append(available_id)
            num = num - 1

        response = self._api.register_targets_to_target_group(self._target_group_arn, target_ids)
        return response

    def decrease_pool_by_size(self, num = 1):
        target_ids = []
        instances_health_status = self.get_registered_instances_health_status()

        for instance_id in instances_health_status:
            if(num <= 0):
                break
            if(instances_health_status[instance_id] in self.get_working_status()):
                target_ids.append({'Id' : instance_id})
                num = num - 1

        response = self._api.deregister_targets_from_target_group(self._target_group_arn, target_ids)
        return response

pool = EC2Pool()
def get_worker_pool():
    return pool
