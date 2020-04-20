"""
Tests for the models in the common application - agency, lake,
species, ect.

"""

import pytest

from .common_factories import (
    LakeFactory,
    ManagementUnitFactory,
    Grid5Factory,
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

    mu_type = "MU"
    label = "A Management Unit"

    lake = LakeFactory(lake_name="Huron", abbrev="HU")
    management_unit = ManagementUnitFactory(label=label, mu_type=mu_type, lake=lake)
    shouldbe = "{} {} {}".format(str(lake), mu_type.upper(), label)
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
