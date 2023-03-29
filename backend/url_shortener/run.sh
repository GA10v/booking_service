#!/bin/sh
flask -A shortener_service.wsgi_app:app db upgrade
uwsgi --strict --ini uwsgi.ini
