import multiprocessing
import os

bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeout
timeout = 120
keepalive = 60

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Logging
accesslog = "/app/logs/access.log"
errorlog = "/app/logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "pdf_ai_app"

# Server mechanics
daemon = False
pidfile = "/app/logs/gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None

# Environment
raw_env = [
    "PYTHONPATH=/app",
]

# Preload app
preload_app = True

# Worker process lifecycle
def on_starting(server):
    server.log.info("Starting PDF AI Application")

def on_reload(server):
    server.log.info("Reloading PDF AI Application")

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    worker.log.info("Worker aborted (pid: %s)", worker.pid)