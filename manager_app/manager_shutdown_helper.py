from manager_app import ec2_pool, aws_api_helper, manager_config, utils
class ManagerShutdownHelper:
    def __init__(self, pool, helper):
        self._pool = pool
        self._aws_helper = helper
        self._hosting_instance_id = manager_config.get_hosting_ec2_id()

    def shutdown_manager(self):
        self.stop_all_running_ec2_instances()
        self._aws_helper.shutdown_ec2_instances_by_ids([self._hosting_instance_id])

    def stop_all_running_ec2_instances(self):
        instances = self._aws_helper.get_running_ec2_instance()
        self._aws_helper.shutdown_ec2_instances_by_ids(utils.prepare_id_in_array_form(instances))

    def start_manager(self):
        instances = self._aws_helper.get_stopped_ec2_instances()
        self._aws_helper.start_ec2_instances_by_ids(utils.prepare_id_in_array_form(instances))

pool = ec2_pool.get_worker_pool()
aws_helper = aws_api_helper.get_api()

shutdown_helper = ManagerShutdownHelper(pool, aws_helper)
def get_manager_shutdown_helper():
    return shutdown_helper
