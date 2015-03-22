"""
Django settings for ecommerce project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2apc_*37r19a627tu(=(t7!91wggkt4#30l59gijmwn67&_^n+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'carts',
    'marketing',
    'orders',
    'products',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'marketing.middleware.DisplayMarketingMessage',
)

ROOT_URLCONF = 'ecommerce.urls'

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Site URL

SITE_URL = "http://localhost:8000"
if DEBUG:
    SITE_URL = "http://localhost:8000"

# User

AUTH_USER_MODEL = 'auth.User'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static_root')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', 'static_files'),
)

# Media

MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')
MEDIA_URL = '/media/'


# Stripe
# Used on server to connect token to publishable key. Pub key on browser; secret in code.
# in separate file for git
from stripe_keys import STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY

STRIPE_SECRET_KEY = STRIPE_SECRET_KEY
STRIPE_PUBLISHABLE_KEY = STRIPE_PUBLISHABLE_KEY


# Email Confirmation
from email_info import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, \
 EMAIL_PORT, EMAIL_BACKEND, EMAIL_USE_TLS, ACCOUNT_EMAIL_VERIFICATION
DEFAULT_FROM_EMAIL = "CFE <twaner23@gmail.com>" #"Coding for Entrepreneuers <cfe@cfe.com>" to Add a name

# sendgrid - transactional emails
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = EMAIL_USE_TLS # contact provider
EMAIL_PORT = EMAIL_PORT # contact provider
EMAIL_BACKEND = EMAIL_BACKEND
ACCOUNT_EMAIL_VERIFICATION=ACCOUNT_EMAIL_VERIFICATION
