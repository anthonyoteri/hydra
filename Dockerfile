FROM node:16-bullseye as nodejs

WORKDIR /app
COPY src/hydra-ui .
RUN yarn
RUN yarn build

FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=0
ENV DJANGO_SETTINGS_MODULE=hydra_core.settings

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /usr/share/nginx/html/*

# Install the backend
WORKDIR /app
COPY src/hydra_core .

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir --requirement=requirements.txt
RUN pip3 install --no-cache-dir .

# Install the frontend
COPY --from=nodejs /app/build /usr/share/nginx/html

# Configure runtime
COPY etc/nginx.conf /etc/nginx/conf.d/default.conf
COPY etc/supervisord.conf /etc/supervisord.conf
COPY docker-entrypoint.sh /usr/bin
EXPOSE 80

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]