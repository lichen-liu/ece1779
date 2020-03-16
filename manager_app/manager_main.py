from flask import render_template, redirect, request
from manager_app import webapp, ec2_pool, pool_monitor_helper, worker_count_monitor, auto_scaler, manager_shutdown_helper, auto_scaler_state_manager
from datetime import datetime
from common_lib import database, s3, utility, combined_aws
import urllib
import requests

@webapp.route('/', methods=['GET','POST'])
def main_handler():
    return render_manager_main_page()

def render_manager_main_page():

    status_by_id = prepare_instance_status_info()
    return render_template('manager_main.html', 
    instances_data_points = prepare_metrics_datapoints(), 
    instance_status_by_id = status_by_id,
    instance_status_text_color = {'healthy':'green', 'unhealthy':'red', 'draining': '#00BFFF', 
    'initial' : '#CCCC00', 'unused' : '#CCCCCC'},
    instances_status_counts = prepare_instance_status_count_info(status_by_id),
    scaler_default_settings = prepare_autoscaler_default_values(),
    dns_status = prepare_dns_status(),
    rds_s3_stats = prepare_rds_s3_stats()
    )

@webapp.route('/api/increase_pool', methods=['POST'])
def increase_pool_handler(num = 1):
    pool = ec2_pool.get_worker_pool()
    pool.increase_pool_by_size(num)
    return redirect('/')

@webapp.route('/api/decrease_pool', methods=['POST'])
def decrease_pool_handler(num = 1):
    pool = ec2_pool.get_worker_pool()
    pool.decrease_pool_by_size(num)
    return redirect('/')

@webapp.route('/api/change_auto_scaler_strategy', methods=['POST'])
def change_auto_scaling_strategy_handler():
    auto_s = auto_scaler.get_auto_scaler()
    auto_s.set_max_threshold(float(request.form.get('max_threshold')))
    auto_s.set_min_threshold(float(request.form.get('min_threshold')))
    auto_s.set_growing_ratio(float(request.form.get('growing_ratio')))
    auto_s.set_shrinking_ratio(float(request.form.get('shrinking_ratio')))
    return redirect('/')

@webapp.route('/api/get_work_count_graph', methods=['POST','GET'])
def get_worker_count_graph_handler():
    monitor = worker_count_monitor.get_worker_count_monitor()
    return render_template('worker_count_graph_page.html', 
    worker_count_by_time = monitor.get_count_status())

@webapp.route('/api/delete_all_user_storage', methods=['POST'])
def delete_all_user_storage():
    combined_aws.delete_all_photos_from_s3_and_database()
    return redirect('/')

@webapp.route('/api/delete_everything', methods=['POST'])
def delete_everything():
    combined_aws.delete_everything_from_s3_and_database()
    return redirect('/')

@webapp.route('/api/stop_all', methods=['POST'])
def stop_all_handler():
    shutdown_helper  = manager_shutdown_helper.get_manager_shutdown_helper()
    shutdown_helper.shutdown_manager()
    return redirect('/')

@webapp.route('/api/toggle_auto_scaler', methods=['POST'])
def toggle_auto_scaler_handler():
    auto_s = auto_scaler.get_auto_scaler()
    auto_s.toggle_scaler()
    return redirect('/')


def prepare_metrics_datapoints():
    '''
    datapoint[instance_id]['CPUUtilization'|'HttpRequestCount'][Datapoints Idx]
    '''
    helper = pool_monitor_helper.get_monitor_helper()
    
    cpu_utilization_info = helper.get_cpu_utilization_for_registered_instances()
    http_request_count_info = helper.get_http_request_count_for_registered_instances()
    
    unified_info = dict()

    # Combine two metrics into one
    for instance_id in cpu_utilization_info:
        unified_info.setdefault(instance_id, dict())['CPUUtilization'] = cpu_utilization_info[instance_id]
    for instance_id in http_request_count_info:
        unified_info.setdefault(instance_id, dict())['HttpRequestCount'] = http_request_count_info[instance_id]
    
    # Process the datapoints
    for instance_id in unified_info:
        for metrics in unified_info[instance_id]:
            unified_info[instance_id][metrics].sort(key = lambda datapoint : datapoint['Timestamp'])
            for datapoint in unified_info[instance_id][metrics]:
                datapoint['Timestamp'] = datapoint['Timestamp'].strftime("%H:%M")

    return unified_info

def prepare_instance_status_info():
    pool = ec2_pool.get_worker_pool()
    instances_status_counts = {}
    return pool.get_registered_instances_health_status()

def prepare_instance_status_count_info(status_by_id):
    instances_status_counts = {}
    for instance_id in status_by_id:
        status_type = status_by_id[instance_id]
        if status_type not in instances_status_counts:
            instances_status_counts[status_type] = 0
        instances_status_counts[status_type] += 1
    return instances_status_counts

def prepare_autoscaler_default_values():
    auto_s = auto_scaler.get_auto_scaler()
    scaler_default_settings = {}
    scaler_default_settings['max_threshold'] = auto_s.get_max_threshold()
    scaler_default_settings['min_threshold'] = auto_s.get_min_threshold()
    scaler_default_settings['growing_ratio'] = auto_s.get_growing_ratio()
    scaler_default_settings['shrinking_ratio'] = auto_s.get_shrinking_ratio()
    status = auto_s.get_running_status()
    if(status):
        scaler_default_settings['running'] = "Disable"
    else:
        scaler_default_settings['running'] = "Enable"

    state = auto_s.get_state()
    if state == auto_scaler_state_manager.ScalerState.READYTORESIZE :
        scaler_default_settings['state'] = 'ready'
    elif state == auto_scaler_state_manager.ScalerState.RESIZING :
        scaler_default_settings['state'] = 'resizing'
    elif state == auto_scaler_state_manager.ScalerState.RESIZINGCOOLDOWN :
        scaler_default_settings['state'] = 'cooldown'
    else:
        scaler_default_settings['state'] = 'none'
    return scaler_default_settings

def prepare_dns_status():
    '''
    (dns_name, dns_is_online)
    '''
    pool = ec2_pool.get_worker_pool()
    dns_name = pool.get_load_balancer_dns_name()

    dns_is_online = False
    try:
        r = requests.head('http://' + dns_name, timeout=5)
        if r.status_code == 200:
            dns_is_online = True
    except Exception:
        pass

    return (dns_name, dns_is_online)


def prepare_rds_s3_stats():
    ece1779_account_num_rows = len(database.get_account_table())
    ece1779_photo_num_rows = len(database.get_photo_table())
    s3_path = s3.ROOT_DIR
    s3_path_size, s3_path_num_directories, s3_path_num_files = s3.get_bucket_content_size(key=s3.ROOT_DIR)
    quote_function = urllib.parse.quote
    return (quote_function, ece1779_account_num_rows, ece1779_photo_num_rows, s3_path, utility.convert_bytes_to_human_readable(s3_path_size), s3_path_num_files, s3_path_num_directories)