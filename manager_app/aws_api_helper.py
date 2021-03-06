import boto3
from datetime import datetime, timedelta

running_ec2_instance_filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        },
        {
            'Name': 'tag:Name',
            'Values' : ['a2-*']
        }
]

stopped_ec2_instance_filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        },
        {
            'Name': 'tag:Name',
            'Values' : ['a2-*']
        }
]

class AwsApiHelper:
    def __init__(self):
        self._ec2_resource = boto3.resource('ec2')
        self._ec2_client = boto3.client('ec2')
        self._elbv2_client = boto3.client('elbv2')
        self._cw_client = boto3.client('cloudwatch')
    
    def get_load_balancers(self):
        return self._elbv2_client.describe_load_balancers()

    def shutdown_ec2_instances_by_ids(self, ids):
        if len(ids):
            self._ec2_client.stop_instances(InstanceIds=ids, DryRun = False)

    def start_ec2_instances_by_ids(self, ids):
        if len(ids):
            self._ec2_client.start_instances(InstanceIds=ids, DryRun = False)

    def get_target_group_on_load_balancer(self, load_balancer_arn):
        return self._elbv2_client.describe_target_groups(LoadBalancerArn = load_balancer_arn)
    
    def get_target_groups(self):
        return self._elbv2_client.describe_target_groups()

    def get_running_ec2_instance(self):
        return self._ec2_resource.instances.filter(Filters=running_ec2_instance_filters)

    def get_stopped_ec2_instances(self):
        return self._ec2_resource.instances.filter(Filters=stopped_ec2_instance_filters)
    
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

    def get_average_cpu_utilization(self, dimensions, sample_num = 30):
        endTime = datetime.utcnow() + timedelta(seconds = 60) # why shifting the entire dataset forward by 60 seconds?
        startTime = endTime - timedelta(seconds = 60 * sample_num)
        return self._cw_client.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=dimensions,
                    StartTime= startTime,
                    EndTime= endTime,
                    Period=60,
                    Statistics=[
                        'Average',
                    ],
                    Unit='Percent'
                )
    
    def get_http_request_per_minute_count(self, dimensions, sample_num = 30):
        endTime = datetime.utcnow() + timedelta(seconds = 60) # why shifting the entire dataset forward by 60 seconds?
        startTime = endTime - timedelta(seconds = 60 * sample_num)
        return self._cw_client.get_metric_statistics(
                    Namespace='ece1779/EC2',
                    MetricName='HttpRequestCount',
                    Dimensions=dimensions,
                    StartTime= startTime,
                    EndTime= endTime,
                    Period=60,
                    Statistics=[
                        'Sum',
                    ],
                    Unit='Count'
                )

api = AwsApiHelper()
def get_api():
    return api
