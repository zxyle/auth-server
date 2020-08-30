#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Zheng <zxyful@gmail.com>
# Desc: Gunicorn configuration file
# gunicorn -c gunicorn.conf.py main:app
# For more detail: http://docs.gunicorn.org/en/latest/settings.html

import multiprocessing

# nginx default.conf Line 21
bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1

# Daemonize the Gunicorn process.
daemon = False

# restart workers when code changes.
reload = True

# process id
pidfile = "/tmp/flask_server.pid"

# logfile
errorlog = "/tmp/flask_server.err"

# the Access log file to write to.
accesslog = "/tmp/flask_server.log"