from flask import render_template, redirect, request
from manager_app import webapp, ec2_pool, pool_monitor_helper, worker_count_monitor, auto_scaler, manager_shutdown_helper
from datetime import datetime
import helper
from common_lib import database, s3, utility
import urllib

@webapp.route('/', methods=['GET','POST'])
def main_handler():
    return render_manager_main_page()

def render_manager_main_page():

    status_by_id = prepare_instance_status_info()
    return render_template('manager_main.html', 
    instances_data_points = prepare_cpu_utilization_info(), 
    instance_status_by_id = status_by_id,
    instance_status_text_color = {'healthy':'green', 'unhealthy':'red', 'draining': '#00BFFF', 
    'initial' : '#CCCC00', 'unused' : '#CCCCCC'},
    instances_status_counts = prepare_instance_status_count_info(status_by_id),
    scaler_default_settings = prepare_autoscaler_default_values(),
    dns_name = prepare_dns_name(),
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
    helper.reset_data()
    return redirect('/')

@webapp.route('/api/delete_everything', methods=['POST'])
def delete_everything():
    helper.reset_all()
    return redirect('/')

@webapp.route('/api/stop_all', methods=['POST'])
def stop_all_handler():
    shutdown_helper  = manager_shutdown_helper.get_manager_shutdown_helper()
    shutdown_helper.shutdown_manager()
    return redirect('/')


def prepare_cpu_utilization_info():
    helper = pool_monitor_helper.get_monitor_helper()
    unordered_utilization_info = helper.get_cpu_utilization_for_registered_instances()
    for instance_id in unordered_utilization_info:
        unordered_utilization_info[instance_id].sort(key = lambda datapoint : datapoint['Timestamp'])
        for datapoint in unordered_utilization_info[instance_id]:
            datapoint['Timestamp'] = datapoint['Timestamp'].strftime("%H:%M")
    return unordered_utilization_info

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
    return scaler_default_settings

def prepare_dns_name():
    pool = ec2_pool.get_worker_pool()
    return pool.get_load_balancer_dns_name()

def prepare_rds_s3_stats():
    ece1779_account_num_rows = len(database.get_account_table())
    ece1779_photo_num_rows = len(database.get_photo_table())
    s3_path = s3.ROOT_DIR
    s3_path_size, s3_path_num_directories, s3_path_num_files = s3.get_bucket_content_size(key=s3.ROOT_DIR)
    quote_function = urllib.parse.quote
    return (quote_function, ece1779_account_num_rows, ece1779_photo_num_rows, s3_path, utility.convert_bytes_to_human_readable(s3_path_size), s3_path_num_files, s3_path_num_directories)