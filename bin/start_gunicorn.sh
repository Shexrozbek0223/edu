#!/bin/bash
source /home/var/projects/edu/venv/bin/activate
exec gunicorn -c "/home/var/projects/edu/gunicorn_conf.py" agrbase.wsgi