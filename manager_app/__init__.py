from flask import Flask

webapp = Flask(__name__)
webapp.config.from_object('manager_app.manager_config.Config')

from manager_app import manager_main, table_query, worker_count_monitor, auto_scaler, manager_shutdown_helper

# Comment out this line to disable authentication
from manager_app import authentication

monitor = worker_count_monitor.get_worker_count_monitor()
monitor.start()

scaler = auto_scaler.get_auto_scaler()
scaler.start()

manager = manager_shutdown_helper.get_manager_shutdown_helper()
manager.start_manager()