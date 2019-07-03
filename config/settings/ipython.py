#same as settings.local - but with

from config.settings.local import *

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
