"""
Django settings for ssp_canvassing project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from unipath import Path
BASE_DIR = Path(os.path.dirname(__file__)).parent.parent

#BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    from secrets import SECRET_KEY
except ImportError:
    print "WARNING: Please create a ssp_canvassing/settings/secrets.py file and add a SECRET_KEY"
    SECRET_KEY = 'w735l4bkg)9k_3!48it^c&f&&l)7+5fp)(768vppge!f1va)_('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_extensions',
    'postcode_locator',
    'core',
    'campaigns',
    'polling',
    'OpenStreetMap',
    'leafleting',
)

MIDDLEWARE_CLASSES = (
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
    from secrets import DATABASES
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = Path(BASE_DIR, 'static')
STATIC_URL = '/static/'
