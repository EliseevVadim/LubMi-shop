from .base import *
import os

DEBUG = False
ADMINS = [('Dmitry', 'dmitry.starushko@gmail.com')]
SITE_URL = "http://192.168.0.100/lms/"
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://192.168.0.100/*']
MEDIA_ROOT = BASE_DIR.parent.parent / 'public_html' / 'media'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'lmshop.sqlite3',
    }
}
