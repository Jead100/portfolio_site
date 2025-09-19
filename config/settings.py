import dj_database_url
import sys
from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool, default=False)

# Toggle admin site availability across dev and prod environments
ADMIN_SITE = config('ADMIN_SITE', cast=bool, default=False)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'jordanead.onrender.com',  # Render domain
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database

DATABASE_URL = config('DATABASE_URL', default='')

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    if not DATABASE_URL:
        raise RuntimeError('DATABASE_URL must be set in production!')
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files & Media (dev defaults)

STATIC_URL = '/static/'

STATICFILES_DIRS = [ BASE_DIR / 'static' ]

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# Prod-only settings
if not DEBUG:
    INSTALLED_APPS += [
        "cloudinary", 
        "cloudinary_storage"
    ]
    
    STATIC_ROOT = BASE_DIR / 'staticfiles'

    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
        'API_KEY': config('CLOUDINARY_API_KEY', default=''),
        'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
    }
    if not all(CLOUDINARY_STORAGE.values()):
        raise RuntimeError(
            "All Cloudinary credentials must be set in production! "
            "Ensure CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, "
            "and CLOUDINARY_API_SECRET are set."
        )

    STORAGES = {
        'default': {
            'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }

    # For cloudinary_storage compatibility (cloudinary_storage's collectstatic 
    # hook expects the old-style STATICFILES_STORAGE setting)
    STATICFILES_STORAGE = STORAGES['staticfiles']['BACKEND']

    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "ERROR"},
}


# Environment Banner (DEV vs PROD)

mode = "DEV" if DEBUG else "PROD"
db_engine = DATABASES["default"]["ENGINE"]
db_name = DATABASES["default"]["NAME"]
color = "\033[92m" if DEBUG else "\033[91m"

print(
    f"{color}[DJANGO STARTUP] Mode={mode}, Engine={db_engine}, DB={db_name}\033[0m",
    file=sys.stderr
)
