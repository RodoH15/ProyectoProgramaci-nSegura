#!/usr/bin/env bash


cd /code
sudo chmod 666 /var/run/docker.sock
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput

gunicorn --bind :8000 programacion.wsgi:application --reload
