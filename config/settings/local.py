from config.settings.base import *

# local settings here.


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DB_PATH = os.path.join(BASE_DIR, 'db/common.db')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_PATH
    }
}
