import sys

__author__ = 'scotm'

from .base import *

INSTALLED_APPS += (
    'debug_toolbar',
    'livereload',
    'debug_toolbar_line_profiler',
)

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar_line_profiler.panel.ProfilingPanel',
]

if 'test' in sys.argv:
    import platform
    if platform.system() == 'Darwin':
        SPATIALITE_LIBRARY_PATH='/usr/local/lib/mod_spatialite.dylib'

    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.spatialite',
            "NAME": ":memory:",
            'TEST_NAME': ":memory:",
        },
    }

    # Disable redirection when testing. https://code.djangoproject.com/ticket/12227
    PREPEND_WWW = False
    TEMPLATE_DEBUG = False
    DEBUG = False
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
