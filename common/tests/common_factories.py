"""
Factories for the models in the common application - agency, lake,
species, ect.

"""

import factory

from ..models import (
    Lake,
    ManagementUnit,
    ManagementUnitType,
    LakeManagementUnitType,
    Grid5,
    Species,
)


class LakeFactory(factory.django.DjangoModelFactory):
    """
    A factory for Lake objects.
    """

    class Meta:
        model = Lake
        django_get_or_create = ("abbrev",)

    abbrev = "HU"
    lake_name = "Huron"


class ManagementUnitTypeFactory(factory.django.DjangoModelFactory):
    """
    A factory for ManagementUnitType objects.
    """

    class Meta:
        model = ManagementUnitType
        django_get_or_create = ("slug",)

    label = "Quota Managemnent Area"
    abbrev = "QMA"
    description = "Management areas used to regulate the commercial fishery."

    @factory.lazy_attribute
    def slug(a):
        return a.abbrev.lower()


class LakeManagementUnitTypeFactory(factory.django.DjangoModelFactory):
    """
    A factory for LakeManagementUnitType objects.
    """

    class Meta:
        model = LakeManagementUnitType
        django_get_or_create = ("lake", "management_unit_type")

    lake = factory.SubFactory(LakeFactory)
    management_unit_type = factory.SubFactory(ManagementUnitTypeFactory)
    primary = False


class ManagementUnitFactory(factory.django.DjangoModelFactory):
    """
    A factory for ManagementUnit objects.
    """

    class Meta:
        model = ManagementUnit

    label = "QMA 4-5"
    description = "A management unit in Lake Huron"
    lake = factory.SubFactory(LakeFactory)
    lake_management_unit_type = factory.SubFactory(LakeManagementUnitTypeFactory)


class Grid5Factory(factory.django.DjangoModelFactory):
    """
    A factory for 5-minute grid objects.
    """

    class Meta:
        model = Grid5

    grid = 1234
    # centroid = GEOSGeometry('POINT(-81.0 45.0)', srid=4326)
    lake = factory.SubFactory(LakeFactory)


class SpeciesFactory(factory.django.DjangoModelFactory):
    """
    A factory for Species objects.
    """

    class Meta:
        model = Species
        django_get_or_create = ("spc",)

    abbrev = "LAT"
    spc_nm = "Lake Trout"
    spc_nmco = "Lake Trout"
    spc_nmsc = "Salvelinus namaycush"
    spc = "081"
    spc_lab = "LaTro"
    spc_nmfam = "SALMONINAE"
    flen2tlen_alpha = 0.0
    flen2tlen_beta = 1.1
