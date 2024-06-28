from .base import *
import os

DEBUG = False
ADMINS = [('Dmitry', 'dmitry.starushko@gmail.com')]
SITE_URL = "http://192.168.0.100/lms/"
ADMIN_DOMAIN = "http://192.168.0.100:8000"
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://192.168.0.100/*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }}
