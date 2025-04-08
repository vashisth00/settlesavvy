# settings.py

import os
from pathlib import Path
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',  # GeoDjango
    
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',  # For token authentication
    'rest_framework_gis',  # For GIS API endpoints
    'corsheaders',
    'leaflet',  # For maps
    'drf_spectacular',  # API documentation
    
    # Custom apps
    'settlesavvy_accounts',
    'settlesavvy_maps',
    'settlesavvy_factors',
    'settlesavvy_api',
]

# Required auth user model setting
AUTH_USER_MODEL = 'settlesavvy_accounts.User'

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Required for admin
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required for admin
    'django.contrib.messages.middleware.MessageMiddleware',  # Required for admin
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settlesavvy_project.urls'

# Templates configuration - required for admin
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'settlesavvy_project.wsgi.application'

# Database Configuration for Supabase
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  # Using PostGIS for geographic data
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': env('DB_PASSWORD', default='Callsup@12345'),
        'HOST': 'db.dfkuygfwrsewjjsrfryf.supabase.co',
        'PORT': '5432',
    }
}

# GeoDjango settings
GDAL_LIBRARY_PATH = '/opt/homebrew/lib/libgdal.dylib'
GEOS_LIBRARY_PATH = '/opt/homebrew/lib/libgeos_c.dylib'

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

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Next.js development server
]

# Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Leaflet Configuration for maps
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (37.8, -96.9),  # Center of the US
    'DEFAULT_ZOOM': 4,
    'MIN_ZOOM': 2,
    'MAX_ZOOM': 18,
}

# Spectacular settings for API documentation
# drf-spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Settle Savvy API',
    'DESCRIPTION': 'API for finding neighborhoods based on preferences',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}