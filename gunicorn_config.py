import multiprocessing

# Bind to localhost on port 8000
bind = "127.0.0.1:8000"

# Number of worker processes (2 * cores + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class - gthread is better for handling multiple requests efficiently
worker_class = "gthread"
threads = 4

# Maximum number of simultaneous clients
worker_connections = 1000

# Timeout for requests
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/log/gunicorn/x-link-access.log"
errorlog = "/var/log/gunicorn/x-link-error.log"
loglevel = "info"

# Process naming
proc_name = "x-link-gunicorn"

# Daemonize the process (set to False if running under systemd)
daemon = False

# Maximum requests before restarting (prevents memory leaks)
max_requests = 1000
max_requests_jitter = 50

# Preload application code
preload_app = True
