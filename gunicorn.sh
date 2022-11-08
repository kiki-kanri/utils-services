#!/bin/bash
. ./env.sh

if [ ! -z $1 ] && [ $1 = "--dev" ]; then
	python3.11 -m gunicorn -b $host:$port --access-logfile '-' --error-logfile '-' --reload -w 1 main.wsgi
else
	python3.11 -m gunicorn -b $host:$port -k "egg:meinheld#gunicorn_worker" -w $workers main.wsgi
fi
