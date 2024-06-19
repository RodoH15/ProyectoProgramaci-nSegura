#!/usr/bin/env bash

#cd /code
#python3 manage.py makemigrations
#python3 manage.py migrate
#python3 manage.py collectstatic --noinput

#gunicorn --bind :8000 programacion.wsgi:application --reload
#!/usr/bin/env bash


cd /code
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput

gunicorn --bind :8000 programacion.wsgi:application --reload
