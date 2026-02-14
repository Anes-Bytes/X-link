"""
Django settings for X-Link project.

This file contains all the configuration for the Django project,
organized by functionality for better maintainability.
"""

import os
from pathlib import Path
from environs import Env

# Environment setup
env = Env()
env.read_env()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)

# Host configuration
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# Security headers (only in production)
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    # Project apps
    'core',
    'cards',
    'Billing',
    'site_management',

    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

# =============================================================================
# MIDDLEWARE CONFIGURATION
# =============================================================================

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
]

if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============================================================================
# URL CONFIGURATION
# =============================================================================

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR}/db.sqlite3')
}




# =============================================================================
# AUTHENTICATION & USER MANAGEMENT
# =============================================================================

AUTH_USER_MODEL = 'core.CustomUser'

# Django Allauth configuration
SITE_ID = env.int('SITE_ID', default=1)
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300  # 5 minutes
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Social account settings
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_STORE_TOKENS = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'SCOPE': [
            'user',
            'read:user',
            'user:email',
        ],
    }
}

SOCIALACCOUNT_ADAPTER = 'core.adapters.CustomSocialAccountAdapter'
ACCOUNT_ADAPTER = 'core.adapters.CustomAccountAdapter'

# Authentication URLs
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/dashboard'
LOGOUT_REDIRECT_URL = '/'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {'user_attributes': ('username', 'email', 'full_name')},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =============================================================================
# INTERNATIONALIZATION & LOCALIZATION
# =============================================================================

LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Persian localization
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# =============================================================================
# TEMPLATES CONFIGURATION
# =============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_context',
            ],
        },
    },
]

# =============================================================================
# CACHE CONFIGURATION
# =============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Cache time settings
LANDING_PAGE_CACHE_TIMEOUT = 60 * 15  # 15 minutes
TEMPLATES_CACHE_TIMEOUT = 60 * 60     # 1 hour
CUSTOMERS_CACHE_TIMEOUT = 60 * 60     # 1 hour

# Session settings - Use cache to reduce DB queries
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@x-link.ir')

# =============================================================================
# MESSAGES CONFIGURATION
# =============================================================================

MESSAGE_TAGS = {
    'DEBUG': 'debug',
    'INFO': 'info',
    'SUCCESS': 'success',
    'WARNING': 'warning',
    'ERROR': 'error',
}

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'cards': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# =============================================================================
# THIRD-PARTY SERVICE CONFIGURATION
# =============================================================================

# SMS service configuration
MELIPAYAMAK_USERNAME = env('MELIPAYAMAK_USERNAME')
MELIPAYAMAK_APIKEY = env('MELIPAYAMAK_APIKEY')
MELIPAYAMAK_NUMBER = env('MELIPAYAMAK_NUMBER')

# Payment gateway (placeholder for future implementation)
PAYMENT_MERCHANT_ID = env('PAYMENT_MERCHANT_ID', default='')

# =============================================================================
# DJANGO DEFAULTS
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin site customization
ADMIN_SITE_HEADER = "پنل مدیریت X-Link"
ADMIN_SITE_TITLE = "مدیریت X-Link"
ADMIN_INDEX_TITLE = "داشبورد مدیریت"

# Debug Toolbar configuration
INTERNAL_IPS = [
    "127.0.0.1",
]
