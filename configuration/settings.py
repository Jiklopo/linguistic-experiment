import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('ENV', 'DEV')
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DOMAINS = json.loads(os.getenv('APP_DOMAINS', '["localhost"]'))
APP_URLS = json.loads(os.getenv('APP_URLS', '["http://localhost"]'))

if ENV == 'DEV':
    SECURITY_LEVEL = 0
elif ENV == 'STAGE':
    SECURITY_LEVEL = 1
elif ENV == 'PROD':
    SECURITY_LEVEL = 2
else:
    SECURITY_LEVEL = 3

DEBUG = ENV == 'DEV'

# Application definition

AUTH_USER_MODEL = 'authentication.User'
ROOT_URLCONF = 'configuration.urls'
WSGI_APPLICATION = 'configuration.wsgi.application'
APPEND_SLASH = False

INTERNAL_IPS = ['127.0.0.1', 'localhost']

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INTERNAL_APPS = [
    'apps.authentication',
    'apps.experiments',
    'apps.common',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'rest_framework',
]

INSTALLED_APPS = [
    'jazzmin',  # admin panel should be before django.contrib.admin
    *DJANGO_APPS,
    *INTERNAL_APPS,
    *THIRD_PARTY_APPS,
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

# Databases
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Caching

ENABLE_CACHE = bool(int(os.getenv('ENABLE_CACHE', '0')))
MEMCACHED_LOCATION = os.getenv('MEMCACHED_LOCATION', None)

if not ENABLE_CACHE:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
elif MEMCACHED_LOCATION:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': MEMCACHED_LOCATION,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'root': {
        'handlers': ['error_file', 'info_file', 'console'],
        'level': LOG_LEVEL,
        'propagate': True
    },

    'handlers': {
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'error.log',
            'level': 'ERROR',
            'formatter': 'verbose',
            'maxBytes': 100 * 1024 * 1024  # 100MB
        },
        'info_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'info.log',
            'level': 'INFO',
            'formatter': 'verbose',
            'maxBytes': 100 * 1024 * 1024  # 100MB
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG' if DEBUG else 'INFO',
            'formatter': 'simple'
        }
    },

    'formatters': {
        'verbose': {
            'format': '{levelname} - {asctime} - {name}:{lineno} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} - {asctime} - {message}',
            'style': '{',
        },
    },
    'filters': {
        'exclude_disallowed_host': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: not record.getMessage().startswith("Invalid HTTP_HOST header:"),
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
            'filters': ['exclude_disallowed_host'],
        },
    },
}

# Security

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-(-$$b=@l@-ntx69+x+xf61yk5r+4j2ln7x)rf@-d@coypvu%oa')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', *APP_DOMAINS]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }
]

JAZZMIN_SETTINGS = {
    "changeform_format": "single",
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ]
}

# Internationalization

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static-back/'
STATIC_ROOT = BASE_DIR / 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'
STATICFILES_DIRS = [
    BASE_DIR / 'static_files'
]

ENABLE_S3 = int(os.getenv('ENABLE_S3', '0'))
if ENABLE_S3:
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': {
                'location': 'media'
            },
        },
        'staticfiles': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': {
                'location': 'static'
            },
        },
    }

# AWS
AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')

AWS_STORAGE_BUCKET_NAME = 'sound_analysis'
AWS_S3_REGION_NAME = 'sgp1'
AWS_DEFAULT_ACL = 'public-read'

# Other
SHELL_PLUS_IMPORTS = [
    'from apps.experiments.single_choice_models import *',
    'from apps.experiments.multiple_choice_models import *',
]