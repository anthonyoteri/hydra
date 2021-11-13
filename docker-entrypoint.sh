#!/bin/bash

python3 /app/manage.py migrate --no-input
python3 /app/manage.py collectstatic

exec $@