#!/bin/sh
python3 manage.py migrate
python3 manage.py createsuperuser --noinput
python3 manage.py collectstatic --noinput
python3 manage.py compilemessages
uwsgi --strict --ini uwsgi/uwsgi.ini
