from .base import *

DEBUG = True
SITE_URL = "http://192.168.0.100:8000/lms/"
ADMIN_DOMAIN = "http://192.168.0.100:8000"
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'lmshop.sqlite3',
    }
}
