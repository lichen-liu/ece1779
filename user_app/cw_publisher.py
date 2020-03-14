import boto3
from datetime import datetime, timedelta
import requests


def get_ec2_instance_id():
    try:
        response = requests.get(url='http://169.254.169.254/latest/meta-data/instance-id', timeout=1)
    except requests.exceptions.Timeout as _:
        return None
    except Exception as e:
        print('Unexpected exception: ' + str(e))
        return None
    else:
        return response.text


def put_http_request_count(count, ec2_instance_id):
    print('count', count)
    print('instance_id', ec2_instance_id)
    _response = boto3.client('cloudwatch').put_metric_data(
        Namespace='ece1779/EC2',
        MetricData=[
            {
                'MetricName': 'HttpRequestCount',
                'Dimensions': [
                    {
                        'Name': 'InstanceId',
                        'Value': ec2_instance_id
                    },
                ],
                'Timestamp': datetime.now(),
                'Value': count,
#                    'StatisticValues': {'SampleCount': count, 'Sum': count, 'Minimum': count, 'Maximum': count},
                'StorageResolution': 60
            },
        ]
    )