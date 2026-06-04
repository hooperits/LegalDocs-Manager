"""
Django settings for legaldocs project.

LegalDocs Manager - A legal document management system.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Load environment variables from .env file
# Path: settings.py -> legaldocs/ -> legaldocs/ -> LegalDocs-Manager/.env
load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')

# Initialize Sentry if DSN is set
SENTRY_DSN = os.getenv('SENTRY_DSN')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
        send_default_pii=True,
    )

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================================
# Security Settings
# =============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if host.strip()
]

# HTTPS and Proxy Security Settings
if not DEBUG:
    # Tell Django it is behind a secure proxy (Nginx terminates SSL)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Enforce cookies to be transmitted over HTTPS only
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS headers
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))  # Default 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Browser security headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# CSRF Trusted Origins (needed in Django 4.0+)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        'CSRF_TRUSTED_ORIGINS',
        'https://localhost,https://127.0.0.1'
    ).split(',')
    if origin.strip()
]



# =============================================================================
# Application Definition
# =============================================================================

INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'drf_spectacular',

    # Local apps
    'api',
    'core',
    'users',
    'clients',
    'cases',
    'documents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS - must be before CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'legaldocs.urls'

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

WSGI_APPLICATION = 'legaldocs.wsgi.application'


# =============================================================================
# Database Configuration
# =============================================================================
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'legaldocs_db'),
        'USER': os.getenv('DB_USER', 'legaldocs_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': int(os.getenv('CONN_MAX_AGE', '0')),
    }
}

# Use SQLite for testing (no CREATE DATABASE permissions needed)
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }


# =============================================================================
# Password Validation
# =============================================================================
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# =============================================================================
# Internationalization
# =============================================================================
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-co'  # Spanish (Colombia)

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True

# Date and time formats for Spanish (DD/MM/YYYY)
DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y H:i:s'
SHORT_DATE_FORMAT = 'd/m/Y'
SHORT_DATETIME_FORMAT = 'd/m/Y H:i'

# DRF date formats
REST_FRAMEWORK_DATE_FORMAT = '%d/%m/%Y'
REST_FRAMEWORK_DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'


# =============================================================================
# Static and Media Files
# =============================================================================
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.getenv('STATIC_ROOT', BASE_DIR / 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =============================================================================
# Default Primary Key Field Type
# =============================================================================
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============================================================================
# Django REST Framework Configuration
# =============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler',
    # Rate limiting - disabled for testing via DISABLE_THROTTLING env var
    'DEFAULT_THROTTLE_RATES': {
        'auth': '1000/min' if os.getenv('DISABLE_THROTTLING') else '5/min',
        'login': '1000/min' if os.getenv('DISABLE_THROTTLING') else '5/min',
        'register': '1000/min' if os.getenv('DISABLE_THROTTLING') else '5/min',
    },
}


# =============================================================================
# CORS Configuration
# =============================================================================

# Development origins - update for production deployment
# For production, replace with actual domain(s):
# CORS_ALLOWED_ORIGINS = ['https://yourdomain.com']
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        'CORS_ALLOWED_ORIGINS',
        'http://localhost:3000,http://127.0.0.1:3000'
    ).split(',')
    if origin.strip()
]

# Allow credentials (cookies, authorization headers)
CORS_ALLOW_CREDENTIALS = True


# =============================================================================
# File Upload Limits and Validation
# =============================================================================

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Maximum file upload size in bytes (10MB)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024

# Allowed file MIME types for document uploads
ALLOWED_FILE_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
    'image/jpeg',
    'image/png',
]


# =============================================================================
# Cache Configuration
# =============================================================================

if 'test' in sys.argv:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': os.getenv('REDIS_URL', 'redis://redis:6379/1'),
        }
    }

# =============================================================================
# Storages Configuration (AWS S3 / MinIO)
# =============================================================================
# In Django 4.2+, the STORAGES setting governs default and static file storage.
USE_S3 = os.getenv('USE_S3', 'False').lower() == 'true'

if 'test' in sys.argv:
    # Use standard FileSystemStorage and clean temp folder for unit testing
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    # Force local media root for tests
    MEDIA_ROOT = BASE_DIR / 'test_media'
elif USE_S3:
    STORAGES = {
        "default": {
            # Use our custom S3 storage class that overrides endpoint resolution for local containers
            "BACKEND": "core.storages.CustomS3Boto3Storage",
            "OPTIONS": {
                "access_key": os.getenv('AWS_ACCESS_KEY_ID'),
                "secret_key": os.getenv('AWS_SECRET_ACCESS_KEY'),
                "bucket_name": os.getenv('AWS_STORAGE_BUCKET_NAME'),
                "region_name": os.getenv('AWS_S3_REGION_NAME', 'us-east-1'),
                "endpoint_url": os.getenv('AWS_S3_ENDPOINT_URL'),
                "file_overwrite": False,
                "default_acl": None,  # S3 best practice (Bucket Owner Enforced)
                "querystring_auth": True,  # Enables secure pre-signed expiring URLs
                "querystring_expire": 3600,  # URLs expire in 1 hour
            },
        },
        "staticfiles": {
            # Keep serving static files locally via Nginx (faster and more secure)
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# =============================================================================
# Rate Limiting Configuration
# =============================================================================

RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'


# =============================================================================
# drf-spectacular (OpenAPI Schema Generation)
# =============================================================================

SPECTACULAR_SETTINGS = {
    'TITLE': 'LegalDocs Manager API',
    'DESCRIPTION': 'API REST para gestión de documentos legales, clientes y casos.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'TAGS': [
        {'name': 'clients', 'description': 'Client management endpoints'},
        {'name': 'cases', 'description': 'Case management endpoints'},
        {'name': 'documents', 'description': 'Document management endpoints'},
    ],
}


# =============================================================================
# Logging Configuration (12-Factor App / Container friendly)
# =============================================================================
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'WARNING',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    }

