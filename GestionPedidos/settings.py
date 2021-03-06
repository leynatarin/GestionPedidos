"""
Django settings for GestionPedidos project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nh6+5$x_52gjixicos+x!+z#a)p+r067h1w-02(&5o^^%vo3s+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_nose',
    'recommends',
    'recommends.tasks',
    'recommends.storages.djangoorm',
    'restaurante',
    'registro',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'GestionPedidos.urls'

WSGI_APPLICATION = 'GestionPedidos.wsgi.application'

AUTH_PROFILE_MODULE = "registro.Perfil"

RECOMMENDS_TASK_RUN = True

RECOMMENDS_TASK_CRONTAB = {'hour': '*/1'}

RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT = 1

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'gestion_pedidos_db',
        'USER':     'leynat',
        'PASSWORD': 'leynat',
        'HOST':     'localhost',
        'PORT':     '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'GestionPedidos/static'),
)

# Los media files son archivos que los usuarios suben: Fotos, Videos, etc

MEDIA_ROOT = os.path.join(BASE_DIR, 'GestionPedidos/media')

MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'GestionPedidos/templates'),
    os.path.join(BASE_DIR, 'restaurante/templates'),
    os.path.join(BASE_DIR, 'registro/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-html-out',
    '--with-coverage',
    '--cover-package=restaurante,registro',
    '--cover-html',
]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'maria.juana.tulua@gmail.com'
EMAIL_HOST_PASSWORD = 'maria.juana'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'maria.juana.tulua@gmail.com'
SERVER_EMAIL = 'maria.juana.tulua@gmail.com'