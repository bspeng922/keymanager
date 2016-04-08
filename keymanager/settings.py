import os

from django.utils.translation import gettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(a62d%3lp15_)cabs4(0mgn)iu5_d2kz8*q@@jgt%891hnm2xz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'managers',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'keymanager.middlewares.RequireLoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'keymanager.urls'

WSGI_APPLICATION = 'keymanager.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'keymanager',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        }
}

SITE_BRANDING = _("Key Manager")
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

PAGE_SIZE = 10

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

LOGIN_REQUIRED_URLS = (
    r"/keys/(.*)$",
    r"/users/(.*)$",
    r"/versions/(.*)$"
)

LOGIN_EXEMPT_URLS = (
    r"/key_available",
    r"/use_key",
    r"/login"
)

VERSIONS = [('standard', _('Standard')),
            ('enterprise', _('Enterprise')),
            ('package', _('Package')),
            ('package_enhanced', _('Package Enhanced'))]

SERVER_LIMIT = [(3, 3), (-1, _('No Limit'))]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))
STATICFILES_DIRS = (
    ("css", os.path.join(BASE_DIR, 'static/css')),
    ("js", os.path.join(BASE_DIR, 'static/js')),
    ("images", os.path.join(BASE_DIR, 'static/images')),
    ("fonts", os.path.join(BASE_DIR, 'static/fonts'))
)

# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# )

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            # Set the level to "DEBUG" for verbose output logging.
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # Logging from django.db.backends is VERY verbose, send to null
        # by default.
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
        },
        'managers.keys.views': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'managers.users.views': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'managers.versions.views': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}