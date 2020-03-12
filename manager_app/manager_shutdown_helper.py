from manager_app import ec2_pool, aws_api_helper, manager_config
class ManagerShutdownHelper:
    def __init__(self, pool, helper):
        self._pool = pool
        self._helper = helper
        self._hosting_instance_id = manager_config.get_hosting_ec2_id()

    def shutdown_manager(self):
        self._pool.stop_and_deregister_all_registerd_instaces()
        self._api.shutdown_ec2_instances_by_ids([self._hosting_instance_id])

pool = ec2_pool.get_worker_pool()
aws_helper = aws_api_helper.get_api()

shutdown_helper = ManagerShutdownHelper(pool, aws_helper)
def get_manager_shutdown_helper():
    return shutdown_helper
