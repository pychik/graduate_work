#!/bin/sh

cmd="$@"

while ! nc -z -v $KAFKA_HOST $KAFKA_PORT;
do
  >&2 echo "Kafka is unavailable, waiting 3 sec!"
  sleep 3;
done

exec $cmd