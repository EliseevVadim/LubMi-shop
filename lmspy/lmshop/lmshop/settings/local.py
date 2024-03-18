from .base import *

DEBUG = True
SITE_URL = "http://192.168.0.100:8000/lms/"
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'lmshop.sqlite3',
    }
}
