# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

import os

from .core import *  # noqa F401

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("PRODUCTION_DB_NAME"),
        "USER": os.getenv("PRODUCTION_DB_USER"),
        "PASSWORD": os.getenv("PRODUCTION_DB_PASSWORD"),
        "HOST": os.getenv("PRODUCTION_DB_HOST"),
        "PORT": os.getenv("PRODUCTION_DB_PORT"),
    }
}
