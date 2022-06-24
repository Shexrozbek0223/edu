#!/bin/bash
source /home/username/var/projects/edu/venv/bin/activate
exec gunicorn -c "/home/username/var/projects/edu/gunicorn_conf.py" agrbase.wsgi
