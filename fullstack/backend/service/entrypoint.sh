#!/bin/bash

python manage.py collectstatic --no-input
python manage.py migrate

nginx

workers=$(($(nproc --all)*2+1))
gunicorn -w $workers -k uvicorn.workers.UvicornWorker --log-level warning -b unix:/tmp/gateway.sock server.asgi:application
