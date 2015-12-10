SECRET_KEY = 'This_is_very_insecure'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
#        'HOST': 'localhost',
        'NAME': 'comrade',
#        'USER': 'canvassing',
#        'PASSWORD': 'm4r13y',
    }
}

# Set up email - Fill out these details
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 465
EMAIL_USE_SSL = True
