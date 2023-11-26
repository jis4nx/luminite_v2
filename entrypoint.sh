#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
if [ "$DEVELOPMENT" = 1 ]; then
	python manage.py runserver 0.0.0.0:8000
else
  gunicorn LuminiteV2.wsgi:application --bind 0.0.0.0:8000
  python manage.py collectstatic --no-input
fi
exec "$@"
