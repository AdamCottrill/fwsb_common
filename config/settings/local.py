from config.settings.base import *


GEOS_LIBRARY_PATH = "c:/OSGeo4W/bin/geos_c.dll"
GDAL_LIBRARY_PATH = "C:/OSGeo4W/bin/gdal204.dll"


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "uglmu_common",
        "USER": get_env_variable("PGUSER"),
        "PASSWORD": get_env_variable("PGPASSWORD"),
        "HOST": "localhost",
    }
}


INSTALLED_APPS = INSTALLED_APPS + ["debug_toolbar"]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# DB_PATH = os.path.join(BASE_DIR, 'db/common.db')
#
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': DB_PATH
#    }
# }
