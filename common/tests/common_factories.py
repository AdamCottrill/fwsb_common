"""
Factories for the models in the common application - agency, lake,
species, ect.

"""

import factory
# from django.contrib.gis.geos import GEOSGeometry

#import common.models as common
from ..models import Lake, ManagementUnit, Grid5, Species

class LakeFactory(factory.DjangoModelFactory):
    """
    A factory for Lake objects.
    """
    class Meta:
        model = Lake
        django_get_or_create = ('abbrev',)

    abbrev = "HU"
    lake_name = "Huron"


class ManagementUnitFactory(factory.DjangoModelFactory):
    """
    A factory for ManagementUnit objects.
    """

    class Meta:
        model = ManagementUnit

    label = 'QMA 4-5'
    description = 'A management unit in Lake Huron'
    lake = factory.SubFactory(LakeFactory)
    mu_type = 'qma'


class Grid5Factory(factory.DjangoModelFactory):
    """
    A factory for 5-minute grid objects.
    """

    class Meta:
        model = Grid5

    grid = '1234'
    #centroid = GEOSGeometry('POINT(-81.0 45.0)', srid=4326)
    lake = factory.SubFactory(LakeFactory)


class SpeciesFactory(factory.DjangoModelFactory):
    """
    A factory for Species objects.
    """

    class Meta:
        model = Species
        django_get_or_create = ('abbrev',)

    abbrev = 'LAT'
    common_name = 'Lake Trout'
    scientific_name = 'Salvelinus namaycush'
    species_code = 81
