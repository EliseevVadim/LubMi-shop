from .base import *
import os

DEBUG = False
ADMINS = [('Dmitry', 'dmitry.starushko@gmail.com')]
SITE_URL = "http://192.168.0.100/lms/"
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://192.168.0.100/*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lms',
        'USER': 'lms',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }}
