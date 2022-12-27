#!/bin/bash

. ./env.sh

baseargs="--no-date-header --no-proxy-headers --no-server-header"
bindargs="--host $host --port $port"

if [ ! -z $1 ] && [ $1 = "--dev" ]; then
	if [ -n $devunix ]; then
		bindargs="--uds $devunix"
	fi

	python3.11 -m uvicorn $baseargs $bindargs --reload main.asgi:app
else
	if [ -n $unix ]; then
		bindargs="--uds $unix"
	fi

	python3.11 -m uvicorn \
		--log-level $loglevel \
		--no-access-log \
		--workers $workers \
		$baseargs \
		$bindargs \
		main.asgi:app
fi
