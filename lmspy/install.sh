#!/bin/bash
docker-compose up -d
docker-compose exec web 'python manage.py migrate --skip-checks'
docker-compose exec web 'python manage.py loaddata lms.json'
docker-compose exec web 'python manage.py createsuperuser'
