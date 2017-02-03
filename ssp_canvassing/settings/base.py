"""
Django settings for ssp_canvassing project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from __future__ import print_function

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from unipath import Path

try:
    import psycopg2
except ImportError:
    # Fall back to psycopg2-ctypes
    from psycopg2cffi import compat

    compat.register()

BASE_DIR = Path(os.path.dirname(__file__)).parent.parent

ADMINS = (
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    from .secrets import SECRET_KEY
except ImportError:
    print("WARNING: Please create a ssp_canvassing/settings/secrets.py file and add a SECRET_KEY")
    SECRET_KEY = 'w735l4bkg)9k_3!48it^c&f&&l)7+5fp)(768vppge!f1va)_('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Attempt to import the email details.
try:
    from .secrets import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_SSL
except ImportError:
    pass

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'flat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_extensions',
    'sortedm2m',
    'postcode_locator',
    'core',
    'campaigns',
    'polling',
    'OpenStreetMap',
    'leafleting',
    'reporting',
    'django_filters',
    'memoize',
)

MIDDLEWARE_CLASSES = (
    # 'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ssp_canvassing.urls'

WSGI_APPLICATION = 'ssp_canvassing.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

try:
    from .secrets import DATABASES
except ImportError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.spatialite',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            Path(BASE_DIR, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'debug': True,
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = Path(BASE_DIR, 'static')
STATIC_URL = '/static/'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
ALL_ALLOWED = False
