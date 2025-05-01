import os, environ

from pathlib import Path

from django.core.management.utils import get_random_secret_key


env = environ.Env()

environ.Env().read_env()

ENV = env('ENV', default='development')

if ENV == 'production':
    SECRET_KEY = env('DJANGO_SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("Production requires DJANGO_SECRET_KEY to be set!")
    DEBUG = False
    print("Using production SECRET_KEY. DEBUG set to False")
else:
    SECRET_KEY = env('DJANGO_SECRET_KEY', default=get_random_secret_key())
    DEBUG = True
    print("⚠️ Using a default development SECRET_KEY. DEBUG set to True. Do not use this in production!")

BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_TRUSTED_ORIGINS = ["https://axion-b6fke8edgahaecgq.eastus2-01.azurewebsites.net/"]
ALLOWED_HOSTS = ["axion-b6fke8edgahaecgq.eastus2-01.azurewebsites.net", "169.254.129.2"]
ALLOWED_REDIRECT_HOSTS = ["axion"]

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/auth/login/'
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'oauth2_provider',

    'App',
    'AuthUser',
    'Entity',
    'Device',
    'Order',
    'MicrosoftAuth',
]

"""AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]"""

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('Templates'))],
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

WSGI_APPLICATION = 'Main.wsgi.application'

if ENV == 'production':
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default=""),
        'USER': env('DB_USER', default=""),
        'PASSWORD': env('DB_PASSWORD', default=""),
        'HOST': env('DB_HOST', default=""),
        'PORT': env('DB_PORT', default=""),
        }
    }
else:
    DATABASES = {
        'default': env.db(default='sqlite:///db.sqlite3')
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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'MicrosoftAuth.authentication.microsoftOauth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rmendoza.abd@gmail.com'
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default="")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "Axion": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
