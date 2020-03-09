import boto3
from datetime import datetime, timedelta

running_ec2_instance_filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
]

class LoadBalancerApis:
    def __init__(self):
        self._ec2_resource = boto3.resource('ec2')
        self._elbv2_client = boto3.client('elbv2')
        self._cw_client = boto3.client('cloudwatch')
    
    def get_load_balancers(self):
        return self._elbv2_client.describe_load_balancers()
    
    def get_target_group_on_load_balancer(self, load_balancer_arn):
        return self._elbv2_client.describe_target_groups(LoadBalancerArn = load_balancer_arn)
    
    def get_target_groups(self):
        return self._elbv2_client.describe_target_groups()

    def get_running_ec2_instance(self):
        return self._ec2_resource.instances.filter(Filters=running_ec2_instance_filters)
    
    def get_health_status_on_group_targets(self, target_group_arn):
        return self._elbv2_client.describe_target_health(TargetGroupArn = target_group_arn)

    def register_targets_to_target_group(self, target_group_arn, target_ids):
        if len(target_ids) > 0:
            return self._elbv2_client.register_targets(TargetGroupArn = target_group_arn,
            Targets = target_ids)

    def deregister_targets_from_target_group(self, target_group_arn, target_ids):
        if len(target_ids) > 0:
            return self._elbv2_client.deregister_targets(TargetGroupArn = target_group_arn,
            Targets = target_ids)

    def get_average_cpu_utilization(self, dimensions):
        return self._cw_client.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=dimensions,
                    StartTime= datetime.now() - timedelta(seconds=60*30),
                    EndTime= datetime.now(),
                    Period=60,
                    Statistics=[
                        'Average',
                    ],
                    Unit='Percent'
                )
    
api = LoadBalancerApis()
def get_api():
    return api