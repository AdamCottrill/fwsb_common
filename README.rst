=====
UGLMU Common
=====


UGLMU Common is a Django application that provides a home for all of
django models used by other UGLMU Django applications. It is build as
an installable application.

Currently, the application includes models, serializers and api
endpoints for lakes, species, 5-minute grids, and management units.

Detailed documentation is in the "docs" directory.

Quick start
-----------

0. > pip install uglmu_common.zip

1. Add "common" and django restframework to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'common',
    ]

2. Include the common URLconf in your project urls.py like this::

    path('common/', include('common.urls')),

3. Add the path to the GEOS and GDAL libraries required by geodjango
   to your settings file:

   GEOS_LIBRARY_PATH = "c:/OSGeo4W/bin/geos_c.dll"
   GDAL_LIBRARY_PATH = "C:/OSGeo4W/bin/gdal204.dll"
    
4. Run `python manage.py migrate` to create the common models.
   
5. Visit http://127.0.0.1:8000/api/v1/common



Associated Resources
--------------------

There are some additional python and sql scripts in the utils
directory that can be used to populate the database.  The sql files
update the geometry fields for each lake, while the python script
updates species, grid5, and management units from the uglmu lookup
tables. Other data sources could be added in the future if needed.

As an alternative to the python and sql scripts which can be run from psql, there
is a common.json fixture that was created using

django-admin dumpdata common --natural-primary --output=utils/common.json

and can be loaded to the database using:

django-admin loaddata common.json



Updating the Application
------------------------


Rebuilding the App.
------------------------

UGLMU common was built as a standard applicaiton can be rebuild for
distrubition following the instructions found here:

https://docs.djangoproject.com/en/2.2/intro/reusable-apps/

With the uglmu-common virtualenv active, and from within the
~/django_common directory, simply run:

> python setup.py sdist

The package will be placed in the ~/dist folder.  To install the
application run the command:

> pip install uglmu_common.zip

To update an existing application issue the command:

> pip install --upgrade uglmu_common.zip


Running the tests
------------------------

UGLMU common contains a number of unit tests that verify that the
application works as expected and that any regregressions are caught
early. The package uses pytest to run all of the tests, which can be
run by issuing the command:

> pytest

After the tests have completed, coverage reports can be found here:

~/htmlcov
