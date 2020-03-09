from flask import render_template, redirect
from app import webapp, load_balancer, cloud_monitor, auto_scaler
from datetime import datetime

@webapp.route('/', methods=['GET','POST'])
def main_handler():
    return render_manager_main_page()

def render_manager_main_page():

    return render_template('manager_main.html', 
    instances_data_points = prepare_cpu_utilization_info(), 
    instances_status_counts = prepare_instance_status_info(),
    scaler_default_settings = prepare_autoscaler_default_values()
    )

@webapp.route('/api/increase_pool', methods=['POST'])
def increase_pool_handler(num = 1):
    lb = load_balancer.get_load_balancer()
    lb.increase_pool_by_size(num)
    return redirect('/')

@webapp.route('/api/decrease_pool', methods=['POST'])
def decrease_pool_handler(num = 1):
    lb = load_balancer.get_load_balancer()
    lb.decrease_pool_by_size(num)
    return redirect('/')

@webapp.route('/api/change_auto_scaler_strategy', methods=['POST'])
def change_auto_scaling_strategy():
    auto_s = auto_scaler.get_auto_scaler()
    return redirect('/')


def prepare_cpu_utilization_info():
    cm = cloud_monitor.get_cloud_monitor()
    unordered_utilization_info = cm.get_cpu_utilization_for_registered_instances()
    for instance_id in unordered_utilization_info:
        unordered_utilization_info[instance_id].sort(key = lambda datapoint : datapoint['Timestamp'])
        for datapoint in unordered_utilization_info[instance_id]:
            datapoint['Timestamp'] = datapoint['Timestamp'].strftime("%H:%M")
    return unordered_utilization_info

def prepare_instance_status_info():
    lb = load_balancer.get_load_balancer()
    instances_status_counts = {}
    instances_health_status = lb.get_registered_instances_health_status()
    for instance_id in instances_health_status:
        status_type = instances_health_status[instance_id]
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




