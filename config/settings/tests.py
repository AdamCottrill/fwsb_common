# usage: python manage.py test pjtk2 --settings=main.test_settings
# flake8: noqa
"""Settings to be used for running tests."""


from config.settings.local import *

SECRET_KEY = "testing"

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

COVERAGE_MODULE_EXCLUDES = ["migrations", "fixtures", "admin$", "utils", "config"]
COVERAGE_MODULE_EXCLUDES += THIRD_PARTY_APPS + DJANGO_APPS
