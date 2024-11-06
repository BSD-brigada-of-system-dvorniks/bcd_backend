#!/bin/sh

# Collect static files
python manage.py collectstatic --noinput

# Adding enviroment variables into system
printenv | grep -v "no_proxy" >> /etc/environment

# Service start
python manage.py runserver
