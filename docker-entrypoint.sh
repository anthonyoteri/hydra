#!/bin/bash

python3 /app/manage.py migrate --no-input
python3 /app/manage.py collectstatic

if [ ! -z "${HYDRA_ROOT_USERNAME}" -a ! -z "${HYDRA_ROOT_PASSWORD}" ]; then
    python3 /app/manage.py createuser --username "${HYDRA_ROOT_USERNAME}" --password "${HYDRA_ROOT_PASSWORD}" --super --ignore-existing
fi

if [ ! -z "${HYDRA_USERNAME}" -a ! -z "${HYDRA_PASSWORD}" ]; then
    python3 /app/manage.py createuser --username "${HYDRA_USERNAME}" --password "${HYDRA_PASSWORD}" --ignore-existing
fi

exec $@