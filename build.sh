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
    else
        echo "Running production tasks..."
        python manage.py migrate
        python manage.py collectstatic --no-input
    fi
fi

exec "$@"

