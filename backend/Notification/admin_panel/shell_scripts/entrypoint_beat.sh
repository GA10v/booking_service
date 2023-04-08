#!/bin/sh
celery -A admin_panel beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler