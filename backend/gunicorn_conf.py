import multiprocessing
import os


host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "80")

# ------------------------------------------------------
# Gunicorn config
# ------------------------------------------------------
bind = f"{host}:{port}"
# 并行工作进程
workers = multiprocessing.cpu_count() * 2 + 1
# 可以使用gevent
worker_class = "uvicorn.workers.UvicornWorker"
# 每个worker的线程数
threads = 2
# 监听队列
blacklog = 2048
# 超时后Worker会被杀掉，并重启。
timeout = 120
graceful_timeout = 120
keepalive = 5
# 设置最大并发
worker_connections = 1000
# 守护进程，交给supervisor管理
deamon = False
loglevel = "info"
accesslog = "./logs/access.log"
"""
其每个选项的含义如下：
h     remote address
l     '-'
u     currently '-', may be user name in future releases
t     date of the request
r     status line (e.g. ``GET / HTTP/1.1``)
s     status
b     response length or '-'
f     referer
a     user agent
T     request time in seconds
D     request time in microseconds
L     request time in decimal seconds
p     process ID
"""
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
pidfile = "./logs/gunicorn.pid"
errorlog = "./logs/error.log"
worker_tmp_dir = "/dev/shm"

# gunicorn -c gunicorn_conf.py main:app -k uvicorn.workers.UvicornWorker
