"""
Tests for the models in the common application - agency, lake,
species, ect.

"""


import pytest
from common.models import LakeManagementUnitType
from django.db.utils import IntegrityError
from django.template.defaultfilters import slugify

from .common_factories import (
    Grid5Factory,
    LakeFactory,
    LakeManagementUnitTypeFactory,
    ManagementUnitFactory,
    ManagementUnitTypeFactory,
    SpeciesFactory,
)


@pytest.mark.django_db
def test_lake_str():
    """
    Verify that the string representation of a Lake object is the lake
    name followed by the lake abbreviation in brackets.
    """

    obj = LakeFactory(lake_name="Huron", abbrev="HU")
    assert str(obj) == "Huron (HU)"


@pytest.mark.django_db
def test_lake_short_name():
    """Verify that the short_name method of our lake model returns just
    the lake name withouth the 'Lake '

    """

    lake = LakeFactory(lake_name="Lake Huron", abbrev="HU")
    assert lake.short_name() == "Huron"


@pytest.mark.django_db
def test_management_unit_str():
    """
    Verify that the string representation of a management unit object
    is the lake, followed by the management unit type, follwed by the label.

    """

    mu_type_abbrev = "MU"
    label = "A Management Unit"
    mu_type = ManagementUnitTypeFactory(abbrev=mu_type_abbrev, label=label)

    lake = LakeFactory(lake_name="Huron", abbrev="HU")
    lake_management_unit_type = LakeManagementUnitTypeFactory(
        lake=lake, management_unit_type=mu_type
    )

    management_unit = ManagementUnitFactory(
        label=label, lake_management_unit_type=lake_management_unit_type, lake=lake
    )
    shouldbe = "{} {} {}".format(str(lake.abbrev), mu_type_abbrev.upper(), label)
    assert str(management_unit) == shouldbe


@pytest.mark.django_db
def test_grid5_str():
    """
    Verify that the string representation of a grid5 object
    is the grid number, followed by the lake abbreviation in brackets.
    """

    lake_abbrev = "HU"
    grid_number = 123
    lake = LakeFactory(lake_name="Huron", abbrev=lake_abbrev)
    grid5 = Grid5Factory(grid=grid_number, lake=lake)
    shouldbe = "{:04d} ({})".format(grid_number, lake_abbrev)
    assert str(grid5) == shouldbe


@pytest.mark.django_db
def test_species_str():
    """
    Verify that the string representation of a species object
    is the species name followed by the species abbreviation in brackets.

    'Walleye (334)'

    """

    spc_nmco = "Walleye"
    spc = "334"
    species = SpeciesFactory(spc_nmco=spc_nmco, spc=spc)
    shouldbe = "{} ({})".format(spc_nmco, spc)
    assert str(species) == shouldbe


@pytest.mark.django_db
def test_management_unit_type_str():
    """The string representation of a managemnet unit type should be
    the label followed by the abbrevation (e.g. - 'Quota Management
    Area (QMA)')"""

    abbrev = "QMA"
    label = "Quota Management Area"
    mu_type = ManagementUnitTypeFactory(abbrev=abbrev, label=label)
    shouldbe = "{} ({})".format(label, abbrev)
    assert str(mu_type) == shouldbe


@pytest.mark.django_db
def test_management_unit_type_save():
    """When we save a management unit type record, a slug should
    automatically created and be a lower case string of label and
    abbreviation. (e.g. -  quota_management_area_qma' )"""

    abbrev = "QMA"
    label = "Quota Management Area"
    mu_type = ManagementUnitTypeFactory(abbrev=abbrev, label=label)
    assert mu_type.slug == slugify(abbrev)


@pytest.mark.django_db
def test_lake_management_unit_type_str():
    """The string representation of a management unit type within a
    lake is the lake abbreviation, folled by the management unit type
    abbrev. (e.g. - 'HU-QMA')"""

    lake_abbrev = "HU"
    lake = LakeFactory(abbrev=lake_abbrev)

    mu_abbrev = "QMA"
    mu_type = ManagementUnitTypeFactory(abbrev=mu_abbrev)

    lake_mu_type = LakeManagementUnitTypeFactory(
        lake=lake, management_unit_type=mu_type
    )
    should_be = "{}-{}".format(lake_abbrev, mu_abbrev)
    assert str(lake_mu_type) == should_be


@pytest.mark.django_db
def test_unique_lake_management_unit_type():
    """Each lake can have only one of each management unit type - if
    we try to create a second 'qma' record for a lake that already has
    a qma management unit type, an error should be thrown.

    """

    lake_abbrev = "HU"
    lake = LakeFactory(abbrev=lake_abbrev)
    qma = ManagementUnitTypeFactory(abbrev="QMA", label="Quota management Area")

    # Don't use factories to create these - it will fetch the existing
    # one instead of trying to create another.
    qma1 = LakeManagementUnitType(lake=lake, management_unit_type=qma, primary=False)

    qma1.save()

    with pytest.raises(IntegrityError):
        qma2 = LakeManagementUnitType(
            lake=lake, management_unit_type=qma, primary=False
        )
        qma2.save()


@pytest.mark.django_db
def test_lake_management_unit_type_save_primary_true():
    """There can only be one management unit type in a lake with
    primary=True. If we try to create a second, an error will be
    thrown by the database when we save it."""

    lake_abbrev = "HU"
    lake = LakeFactory(abbrev=lake_abbrev)

    qma = ManagementUnitTypeFactory(abbrev="QMA", label="Quota management Area")
    LakeManagementUnitTypeFactory(lake=lake, management_unit_type=qma, primary=True)

    ltrz = ManagementUnitTypeFactory(abbrev="LTRZ", label="Lake Trout Rehab Zone")

    with pytest.raises(IntegrityError):
        LakeManagementUnitTypeFactory(
            lake=lake, management_unit_type=ltrz, primary=True
        )


@pytest.mark.django_db
def test_lake_management_unit_type_save_primary_false():
    """there can by an arbriary number of management unit types
    assocaiated with a lake as long as there is only one with
    'primary'=True"""

    lake_abbrev = "HU"
    lake = LakeFactory(abbrev=lake_abbrev)

    mu_type = ManagementUnitTypeFactory(abbrev="QMA", label="Quota management Area")
    LakeManagementUnitTypeFactory(
        lake=lake, management_unit_type=mu_type, primary=False
    )

    mu_type = ManagementUnitTypeFactory(abbrev="LTRZ", label="Lake Trout Rehab Zone")

    LakeManagementUnitTypeFactory(
        lake=lake, management_unit_type=mu_type, primary=False
    )
