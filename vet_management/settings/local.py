from os import path, getenv
from pathlib import Path
from dotenv import load_dotenv

from .base import * # noqa
from .base import BASE_DIR

local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)

DEBUG = True
SITE_NAME = getenv("SITE_NAME")
SECRET_KEY = getenv("DJANGO_SECRET_KEY", "e3dbaff8767429783455e3939686ae4d19fa79b3e2138a25e6f4ca3066b95b9d73279a5a5df6607e34aacde9bb184ceb9c53d71d2c909cf5d4848d3e028330392a0deccc36964638c7e075659f5f4f5a1bae3830c09459f3c50560244decbeff6e0c8548")

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

ADMIN_URL = getenv("DJANGO_ADMIN_URL")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}