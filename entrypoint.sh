#!/bin/sh
set -e
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py createsuperuser --noinput --username "${DJANGO_SUPERUSER_USERNAME}" --email "${DJANGO_SUPERUSER_EMAIL}" 2>/dev/null || true
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2