"""
Django settings for TAEN project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'False':
    DEBUG = False
else:
    DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = [
            'www.entertaen.com',
            'entertaen.com',
    ]

SITE_ID = 1


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'TAEN_APP.apps.TaenAppConfig',
    'registration',
    'storages',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TAEN.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'registration'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TAEN.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'entertaen',
            'USER': 'admin',
            'PASSWORD': 'password',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }


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

# These settings set up email sending which prints out the email in the terminal - Needs to change before release - use format below
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'support@entertaen.com'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    DEFAULT_FROM_EMAIL = 'support@entertaen.com'
    EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
    EMAIL_HOST_USER = os.environ['AWS_SES_ACCESS_KEY_ID']
    EMAIL_HOST_PASSWORD = os.environ['AWS_SES_SECRET_KEY']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static', 'images'),
        os.path.join(BASE_DIR, 'static', 'css'),
        os.path.join(BASE_DIR, 'static', 'js'),
        os.path.join(BASE_DIR, 'static', 'fonts'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if DEBUG:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
else:
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
                    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
                            'Cache-Control': 'max-age=94608000',
                            }
    AWS_STORAGE_BUCKET_NAME = 'taenstatic'
    AWS_ACCESS_KEY_ID = os.environ['AWS_IAM_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_IAM_SECRET_KEY']
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    STATICFILES_LOCATION = 'static'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

    MEDIA_URL = '/media/'
    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'


PASSWORD_HASHERS = (
                'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
                'django.contrib.auth.hashers.BCryptPasswordHasher',
                'django.contrib.auth.hashers.PBKDF2PasswordHasher',
                'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/home/'
