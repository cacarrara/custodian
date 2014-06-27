"""
Django settings for custodian project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

TEMPLATE_DEBUG = config('TEMPLATE_DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []

ADMINS = (
    ('Caio Carrara', 'caiocarrara@gmail.com'),
)


# Application definition
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'custodian.urls'

WSGI_APPLICATION = 'custodian.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':   config('DATABASE_ENGINE'),
        'NAME':     config('DATABASE_NAME'),
        'USER':     config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST':     config('DATABASE_HOST'),
        'PORT':     config('DATABASE_PORT'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SUIT_CONFIG = {
    'ADMIN_NAME': 'Custodian - Basic Financial Management',
    'SEARCH_URL': '',
    'MENU': (
        'sites',
        'auth',
        '-',
        {'label': 'Registers', 'icon': 'icon-cog',
            'models': ('core.payable',
                        'core.receivable',
                        'core.person', 
                        'core.account',
                        'core.businesssegment',
            )
        },
        {'label': 'Operations', 'icon': 'icon-pencil',
            'models': ('core.expense', 'core.revenue',)},
        '-',
        {'label': 'Dashboard', 'icon': 'icon-th', 
            'url': '/admin/dashboard'},
        '-',
    ),
}