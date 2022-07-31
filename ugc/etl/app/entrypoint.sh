#!/bin/sh
cmd="$@"
while ! nc -z -v $CH_HOST $CH_PORT;
do
  >&2 echo "ClickHouse is unavailable, waiting 3 sec!"
  sleep 3;
done
exec $cmd