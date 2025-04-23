# gunicorn.conf.py

bind = "0.0.0.0:8000"
workers = 3
timeout = 120
graceful_timeout = 30
keepalive = 5
errorlog = "-"
accesslog = "-"
loglevel = "info"
