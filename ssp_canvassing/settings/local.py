import sys

__author__ = 'scotm'

from .base import *

INTERNAL_IPS = ('127.0.0.1',)

if 'test' in sys.argv:
    import platform

    SPATIALITE_LIBRARY_PATH = 'mod_spatialite'
    if platform.system() == 'Darwin':
        SPATIALITE_LIBRARY_PATH = '/usr/local/lib/mod_spatialite.dylib'

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

    # Remove unnecessary apps
    apps_to_remove = {'flat', 'django.contrib.admin', 'django_extensions', 'OpenStreetMap', }
    INSTALLED_APPS = tuple(filter(lambda x: x not in apps_to_remove, INSTALLED_APPS))

    # Don't bother testing migrations - https://gist.github.com/NotSqrt/5f3c76cd15e40ef62d09
    class DisableMigrations(object):
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return "notmigrations"


    MIGRATION_MODULES = DisableMigrations()
else:
    INSTALLED_APPS += (
        'debug_toolbar',
        'livereload',
        'debug_toolbar_line_profiler',
    )
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
