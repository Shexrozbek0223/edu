command = '/home/username/var/projects/edu/bin/gunicorn'
pythonpath = '/home/var/projects/edu/'
bind = '0.0.0.0:8801'
workers = 3
user = 'username'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=agrbase.settings'
