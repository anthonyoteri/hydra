FROM python:3.10.0-slim

ENV LANG en_US.utf8
ENV LC_ALL en_US.utf8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PIP_NO_CACHE_DIR=0

ENV DJANGO_SETTINGS_MODULE=hydra_core.settings

EXPOSE 8000

WORKDIR /app

COPY . .
COPY requirements.txt ./
RUN pip3 install --requirement=requirements.txt
RUN pip3 install .

CMD ["python", "manage.py", "serve", "0.0.0.0:8000"]