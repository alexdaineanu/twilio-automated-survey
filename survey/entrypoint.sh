#!/usr/bin/bash

python manage.py migrate
watchmedo auto-restart --directory=./ --pattern=*tasks.py --recursive -- celery -A survey worker  --loglevel=INFO  &
python manage.py runserver 0.0.0.0:80
