#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
        sleep 0.1
    done

    echo "PostgreSQL started"

    if [ "$DEVELOPMENT" = "1" ]
	then
        echo "Running development tasks..."
        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver 0.0.0.0:8000
    else
        echo "Running production tasks..."
        python manage.py migrate
        python manage.py collectstatic --no-input
        gunicorn LuminiteV2.wsgi:application --bind 0.0.0.0:8000
    fi
fi

exec "$@"

