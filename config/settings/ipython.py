# same as settings.local - but with

from config.settings.local import *

DEBUG = True

SECRET_KEY = get_env_variable("SECRET_KEY")
