"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from urllib.parse import urlparse

import mongoengine
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR.parent / ".env"

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-ecu4&$k&!nndfp7ae0r_03l1+&-zo0xu=8te3e9v7+p!p^%p42")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_crontab',
    'bots.apps.BotsConfig',
    'manga.apps.MangaConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
REDIS_URL = os.environ.get("REDIS_TLS_URL") or os.environ.get("REDIS_URL", "127.0.0.1:6379")
REDIS_URL_SEGMENTS = REDIS_URL.split(":")
REDIS_HOST, REDIS_PORT = ":".join(REDIS_URL_SEGMENTS[:-1]), int(REDIS_URL_SEGMENTS[-1])

DATABASES = {
    "default": {},
    "mongodb": {
        "NAME": os.environ.get("MONGODB_NAME"),
        "HOST_NAME": os.environ.get("MONGODB_HOST_NAME"),
        "USERNAME": os.environ.get("MONGODB_USERNAME"),
        "PASSWORD": os.environ.get("MONGODB_PASSWORD"),
    },
    "redis": {
        "HOST": REDIS_HOST,
        "PORT": REDIS_PORT,
        "DB": int(os.environ.get("REDIS_DB", 0)),
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = './src/static'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Env variable
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
DISCORD_USER_ID = int(os.environ.get("DISCORD_USER_ID", 0))

CRONJOBS = [
    ('*/30 * * * *', 'manga.jobs.run_manga_parser.run_manga_parser')
]

# Connect to MongoDB server
mongoengine.connect(
    db=DATABASES["mongodb"]["NAME"],
    host=DATABASES["mongodb"]["HOST_NAME"],
    username=DATABASES["mongodb"]["USERNAME"],
    password=DATABASES["mongodb"]["PASSWORD"],
)
