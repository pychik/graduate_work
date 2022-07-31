#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

flask db upgrade
flask init-roles
flask init-admin
gunicorn -k gevent wsgi:app --bind 0.0.0.0:8000 --reload
exec "$@"