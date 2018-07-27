#!/bin/bash

now=`pwd`
dir=`dirname $0`
pid=uwsgi.pid
log=logs/uwsgi.log

cd $dir
path=`echo \`pwd\` | awk -F '/' '{print $NF}'`

usage(){
  echo -e '\033[31m'
  echo -e 'Usage:'
  echo -e '	uwsgi.sh [start|stop|restart]'
  echo -e '\033[0m'
}

start(){
  uwsgi3 --ini config.ini --pyargv $path
  sleep 1
  num=`grep -n 'Starting uWSGI' $log | gawk -F ':' '{print $1}' | tail -n 1`
  sed -n $num',$p' $log
}

stop(){
  kill -9 `ps aux | grep uwsgi3 | grep $path | grep -v grep | awk '{print $2}'`
}

state(){
  ps aux | grep uwsgi3 | grep $path | grep -v grep
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
