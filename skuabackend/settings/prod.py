
"""
Production server settings.
"""

from .base import *
from dotenv import load_dotenv

load_dotenv(".env.prod")

DEBUG = False
ALLOWED_HOSTS = []

# PostgreSQL Database 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

# JWT Settings
JWT_SETTINGS = {
    'SECRET_KEY': os.getenv('JWT_SECRET_KEY'),
    'ALGORITHM': os.getenv('JWT_ALGORITHM'),
    'ACCESS_TOKEN_LIFETIME': 5,
    'REFRESH_TOKEN_LIFETIME': 7, 
    'TOKEN_TYPE_CLAIM': 'type',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_TYPE_ACCESS': 'access',
    'TOKEN_TYPE_REFRESH': 'refresh', 
}

# Enable Django Debug Toolbar if needed
INSTALLED_APPS += [
                # 'debug_toolbar',

                # User Defined Apps
                # 'api',
                # 'organization',
                # 'users',
                # 'userauth',
                ]
# MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')

CORS_ALLOWED_ORIGINS += []

INTERNAL_IPS = []
