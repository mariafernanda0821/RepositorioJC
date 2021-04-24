from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'JC06',
        'USER': 'postgres',
        'PASSWORD': '123456789',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = ['static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

#email settings
EMAIL_USE_TLS = True
EMAIL_HOST ='smtp.gmail.com'
EMAIL_HOST_USER = 'sanjosecondominio21@gmail.com'
DEFAULT_FROM_EMAIL = 'sanjosecondominio21@gmail.com'
SERVER_EMAIL = 'sanjosecondominio21@gmail.com'
EMAIL_HOST_PASSWORD ='tsjcon21*'
EMAIL_PORT = 587

