from flask import Flask

webapp = Flask(__name__)

from manager_app import manager_main, worker_count_monitor, auto_scaler

monitor = worker_count_monitor.get_worker_count_monitor()
monitor.start()

scaler = auto_scaler.get_auto_scaler()
scaler.start()