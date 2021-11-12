FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=0
ENV DJANGO_SETTINGS_MODULE=hydra_core.settings

RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
  && rm -rf /var/lib/apt/lists/*

COPY etc/nginx.conf /etc/nginx/conf.d/default.conf
COPY etc/supervisord.conf /etc/supervisord.conf

WORKDIR /app
COPY src/hydra_core .

RUN pip3 install --no-cache-dir --requirement=requirements.txt
RUN pip3 install .

COPY docker-entrypoint.sh /usr/bin
EXPOSE 80

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
