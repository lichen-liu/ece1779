from flask import render_template, redirect
from app import webapp, load_balancer, cloud_monitor

@webapp.route('/', methods=['GET','POST'])
def main_handler():
    return render_manager_main_page()

def render_manager_main_page():
    return render_template('manager_main.html')

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

@webapp.route('/api/get_cpu_utilization', methods=['POST'])
def get_cpu_utilization_handler():
    cm = cloud_monitor.get_cloud_monitor()
    print(cm.get_cpu_utilization_for_registered_instances())
    return redirect('/')

