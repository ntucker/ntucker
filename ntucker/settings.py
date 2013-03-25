# Django settings for ntucker project.
from __future__ import unicode_literals
import os.path
import dj_database_url

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

try:
    from local_settings import DEBUG
except ImportError:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Nathaniel Tucker', 'natmaster@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': dj_database_url.config()
}
DATABASES['default']['OPTIONS'] = {'autocommit': True,}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'US/Pacific'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

STATIC_URL = "https://s3.amazonaws.com/ntucker.me/"
STATIC_ROOT = STATIC_URL
MEDIA_URL = STATIC_URL + "media/"


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(PROJECT_ROOT, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Django Storages/S3 Settings
DEFAULT_FILE_STORAGE = 'utils.s3backend.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'utils.s3backend.StaticRootS3BotoStorage'

# AWS Settings
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'ntucker.me'
AWS_HEADERS = {
               b'Expires': b'Thu, 15 Apr 2020 20:00:00 GMT',
               b'Cache-Control': b'max-age=86400',
               }
from boto.s3.connection import ProtocolIndependentOrdinaryCallingFormat
AWS_S3_CALLING_FORMAT = ProtocolIndependentOrdinaryCallingFormat()
AWS_QUERYSTRING_AUTH = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7g8yomr^&tx9ut=hhl4mk%*#eld64k!h13$i&luuy1k3by$i(v787yhuhnj'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "cms.context_processors.media",
    "sekizai.context_processors.sekizai",
    "django.core.context_processors.request",
)

CMS_TEMPLATES = (
    ('index.html', 'Index'),
    ('simple.html', 'Simple'),
    ('four.html', 'Four blocks'),
    ('two.html', 'Two blocks'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

ROOT_URLCONF = 'ntucker.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ntucker.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'storages',
    'south',
    'django.contrib.sitemaps',
    
    #cms stuff
    'cms',
    'mptt',
    'menus',
    'sekizai',
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.link',
    'cms.plugins.file',
    'cms.plugins.teaser',
    'cms.plugins.video',
    'cms.plugins.googlemap',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
