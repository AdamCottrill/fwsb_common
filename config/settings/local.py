from config.settings.base import *

# install gdal in virtualenv:
VIRTUAL_ENV = os.environ["VIRTUAL_ENV"]
OSGEO_VENV = os.path.join(VIRTUAL_ENV, "Lib/site-packages/osgeo")
GEOS_LIBRARY_PATH = os.path.join(OSGEO_VENV, "geos_c.dll")
GDAL_LIBRARY_PATH = os.path.join(OSGEO_VENV, "gdal304.dll")
PROJ_LIB = os.path.join(VIRTUAL_ENV, "Lib/site-packages/osgeo/data/proj")

os.environ["GDAL_DATA"] = os.path.join(VIRTUAL_ENV, "Lib/site-packages/osgeo/data/gdal")
os.environ["PROJ_LIB"] = PROJ_LIB
os.environ["PATH"] += os.pathsep + str(OSGEO_VENV)

geolibs = [
    ("OSGEO_VENV", OSGEO_VENV),
    ("GEOS_LIBRARY_PATH", GEOS_LIBRARY_PATH),
    ("GDAL_LIBRARY_PATH", GDAL_LIBRARY_PATH),
    ("PROJ_LIB", PROJ_LIB),
]

for lib in geolibs:
    if not os.path.exists(lib[1]):
        print("Unable to find {} at {}".format(*lib))


SECRET_KEY = get_env_variable("SECRET_KEY")

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
