#!/bin/bash

echo "⏳ Running database migrations..."
python manage.py migrate --noinput

echo "✅ Migrations applied. Starting server..."
exec gunicorn axion.wsgi:application --bind 0.0.0.0:8000
