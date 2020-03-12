from flask import Flask

webapp = Flask(__name__)

from manager_app import manager_main, worker_count_monitor, auto_scaler, manager_shutdown_helper

monitor = worker_count_monitor.get_worker_count_monitor()
monitor.start()

scaler = auto_scaler.get_auto_scaler()
scaler.start()

manager = manager_shutdown_helper.get_manager_shutdown_helper()
manager.start_manager()