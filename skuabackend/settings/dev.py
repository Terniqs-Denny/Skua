
"""
Development server settings.
"""

from .base import *
from dotenv import load_dotenv

load_dotenv(".env.dev")

DEBUG = True  # Enable debugging in dev

ALLOWED_HOSTS = ['*'] #use domain name here

# PostgreSQL Database for Development Server
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
    'ACCESS_TOKEN_LIFETIME': 120,
    'REFRESH_TOKEN_LIFETIME': 7, 
    'TOKEN_TYPE_CLAIM': 'type',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_TYPE_ACCESS': 'access',
    'TOKEN_TYPE_REFRESH': 'refresh', 
}

# Logging (optional)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
