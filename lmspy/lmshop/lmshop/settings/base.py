from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-ndk$^6524i$_@bh($4-tudm^iou3i-#t*2tcuf%%85aptweu-p'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lms.apps.LmsConfig',
    'customerinfo.apps.CustomerInfoConfig',
    'djmoney',
    'easy_thumbnails',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lms.api.middleware.axios_crutches',
]

ROOT_URLCONF = 'lmshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'lms.processors.processors.parameters_processor',
                'lms.processors.processors.payment_processor',
                'lms.processors.processors.scui_processor',
                'lms.processors.processors.shorts_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'lmshop.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

USE_THOUSAND_SEPARATOR = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer', 'rest_framework.renderers.BrowsableAPIRenderer'],
    # Next turns off CSRF! ------------------------------------
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/day',
        'user': '10000/day'
    }
    # ---------------------------------------------------------
}

CUSTOMER_INFO_SESSION_ID = 'customer-info-session-v1'

SEARCH_INPUT_RGX = '^[А-Яа-яЁё0-9 -]+$'

PACKAGE_WIDTH_CM = 30

PACKAGE_LENGTH_CM = 40

PACKAGE_UNIT_HEIGHT_CM = 5

SLEEP_AFTER = 4
