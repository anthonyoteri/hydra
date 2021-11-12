#!/bin/bash

DEBUG=0 python3 /app/manage.py migrate --no-input

exec $@