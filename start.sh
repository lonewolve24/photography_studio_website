#!/bin/bash
set -e
cd "$(dirname "$0")/photostudio_backend"
python manage.py migrate
python manage.py collectstatic --noinput
exec gunicorn photostudio_backend.wsgi --bind "0.0.0.0:${PORT:-8000}" --timeout 120
