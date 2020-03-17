from datetime import timedelta

HOSTING_EC2_INSTANCE_ID = 'i-01247d748caf64ae6'
DEFAULT_LOAD_BALANCER_INDEX = 0
DEFAULT_TARGET_GROUP_INDEX = 0
MIN_WORKER_NUM = 1
def get_hosting_ec2_id():
    return HOSTING_EC2_INSTANCE_ID
def get_default_load_balancer_index():
    return DEFAULT_LOAD_BALANCER_INDEX
def get_default_target_group_index():
    return DEFAULT_TARGET_GROUP_INDEX
def get_min_worker_num():
    return MIN_WORKER_NUM


class Config(object):
    SECRET_KEY = 'ZHEGESECRETKEYYIDIANYEBUANQUAN'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes= 60)
    SESSION_REFRESH_EACH_REQUEST = False
