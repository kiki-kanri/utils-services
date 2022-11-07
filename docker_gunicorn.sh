#!/bin/bash
. ./env.sh

gunicorn -b 0.0.0.0:8000 -k "egg:meinheld#gunicorn_worker" -w $workers main.wsgi