FROM node:17.2.0-alpine3.12 as nodejs

WORKDIR /app

# Workaround for "digital envelope routines::unsupported" error
ENV NODE_OPTIONS=--openssl-legacy-provider

COPY src/hydra-ui/package.json src/hydra-ui/yarn.lock ./
RUN yarn install --frozen-lockfile --non-interactive

COPY src/hydra-ui .
RUN yarn build

FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=0
ENV DJANGO_SETTINGS_MODULE=hydra_core.settings

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    nginx \
    supervisor \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /usr/share/nginx/html/*

# Install the backend
WORKDIR /app
COPY src/hydra-core .

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir --requirement=requirements.txt
RUN pip3 install --no-cache-dir .

# Install the frontend
COPY --from=nodejs /app/build /usr/share/nginx/html

# Configure runtime
RUN rm /etc/nginx/sites-enabled/*
COPY etc/nginx.conf /etc/nginx/conf.d/default.conf
COPY etc/supervisord.conf /etc/supervisord.conf
COPY docker-entrypoint.sh /usr/bin
EXPOSE 80

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
