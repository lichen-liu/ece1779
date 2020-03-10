from flask import Flask

webapp = Flask(__name__)

from app import manager_main, worker_count_monitor

monitor = worker_count_monitor.get_worker_count_monitor()
monitor.start()
