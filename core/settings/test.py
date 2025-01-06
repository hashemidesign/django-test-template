import os

from .core import *  # noqa F401

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("TEST_DB_NAME"),
        "USER": os.getenv("TEST_DB_USER"),
        "PASSWORD": os.getenv("TEST_DB_PASSWORD"),
        "HOST": os.getenv("TEST_DB_HOST"),
        "PORT": os.getenv("TEST_DB_PORT"),
    },
}
