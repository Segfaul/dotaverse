# gunicorn configuration file
import os

bind = '0.0.0.0:8000'

workers = 4
worker_class = 'uvicorn.workers.UvicornWorker'
timeout = 30
keepalive = 2

errorlog = '-'
accesslog = os.getenv('LOG_FILE_PATH', 'dotaverse.log')
loglevel = 'warning'
acess_log_format = '[%(asctime)s: %(levelname)s/%(name)s] %(message)s'
