#!/bin/sh
cmd="$@"
while true;
if ! nc -z -v $CH_HOST $CH_PORT and ! nc -z -v $MONGO_HOST $MONGO_PORT (goto done) else (goto do)
do
  >&2 echo "Databases is not available, waiting 3 sec!"
  sleep 3;
done
exec
$cmd