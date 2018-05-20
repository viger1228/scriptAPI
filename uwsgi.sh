#!/bin/bash

now=`pwd`
dir=`dirname $0`
pid=uwsgi.pid
log=logs/uwsgi.log

cd $dir

usage(){
  echo -e '\033[31m'
  echo -e 'Usage:'
  echo -e	'	uwsgi.sh [start|stop|restart]'
  echo -e '\033[0m'
}

start(){
  uwsgi3 --ini config.ini
  sleep 1
  num=`grep -n 'Starting uWSGI' $log | gawk -F ':' '{print $1}' | tail -n 1`
  sed -n $num',$p' $log
}

stop(){
  pkill -9 uwsgi3
}

state(){
  ps -ef | grep uwsgi3 | grep -v grep
}


if [ $# != 1 ]; then
  usage
elif [ $1 == 'start' ]; then
  start
elif [ $1 == 'stop' ]; then
  stop
elif [ $1 == 'state' ]; then
  state
elif [ $1 == 'restart' ]; then
  stop
  sleep 1
  start
else
  usage
fi

cd $now
