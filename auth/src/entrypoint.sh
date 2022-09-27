#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    while ! nc -z $KAFKA_URL; do
      sleep 3
    done

    echo "PostgreSQL and Kafka services started"
fi
exec "$@"