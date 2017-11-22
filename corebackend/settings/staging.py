from .base import *
ALLOWED_HOSTS = ['104.236.217.40',]
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'conegpstagingdb',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/staticfiles/'
APPSECRET_PROOF = False
