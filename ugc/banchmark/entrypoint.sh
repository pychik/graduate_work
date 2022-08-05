#!/bin/sh
cmd="$@"
ACCESS=false

while ! $ACCESS;
do
  CONNECT_CH= nc -z -v $CH_HOST $CH_PORT
  CONNECT_MD= nc -z -v $MONGO_HOST $MONGO_PORT
  if [ ! CONNECT_CH ] && [ ! CONNECT_MD ];
  then
    >&2 echo "Databases is not available, waiting 3 sec!"
    sleep 3;
  else
    ACCESS=true
  fi
done
exec
$cmd