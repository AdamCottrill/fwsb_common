"""=============================================================
~/uglmu_common/common/tests/api/test_management_units.py
 Created: 18 Apr 2020 09:30:08

 DESCRIPTION:

  Tests for the api end points for Management Units

  Management Units detail should include: label, mu-type, slug, lake,
  centroid, and envelope (optionaly someday, it could also inlcude
  geom)

  Management Units list should return all management unit objects. The
  fields returned are exactly the same as the detailed endpoint.
  There are currently filters for lake and management unit type
  (mu_type)

 A. Cottrill
=============================================================

"""

import pytest
from common.models import ManagementUnit
from django.contrib.gis.geos import GEOSGeometry
from django.urls import reverse
from rest_framework import status

from ..common_factories import (
    LakeFactory,
    LakeManagementUnitTypeFactory,
    ManagementUnitFactory,
    ManagementUnitTypeFactory,
)


@pytest.fixture()
def polygonA():
    """A polygon somewhere in Lake Huron."""

    wkt = (
        "MULTIPOLYGON(((-82.0 44.0,"
        + "-82.5 44.0,"
        + "-82.5 44.5,"
        + "-82.0 44.5,"
        + "-82.0 44.0)))"
    )
    return GEOSGeometry(wkt.replace("\n", ""), srid=4326)


@pytest.fixture()
def manUnitList(polygonA):
    """a List of mangement unit objects - two differnt types from two
    different lakes.
    """

    # lakes
    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
    erie = LakeFactory(abbrev="ER", lake_name="Lake Erie")

    # management unit types
    qma = ManagementUnitTypeFactory(label="Quota Managemnent Area", abbrev="QMA")
    aa = ManagementUnitTypeFactory(label="Assessment Area", abbrev="AA")

    # lake management unit types
    huron_mu1 = LakeManagementUnitTypeFactory(lake=huron, management_unit_type=qma)
    huron_mu2 = LakeManagementUnitTypeFactory(lake=huron, management_unit_type=aa)
    erie_mu = LakeManagementUnitTypeFactory(lake=erie, management_unit_type=aa)

    huron_qma = ManagementUnitFactory(
        lake=huron, label="QMA-00", geom=polygonA, lake_management_unit_type=huron_mu1
    )
    huron_qma.save()

    huron_aa = ManagementUnitFactory(
        lake=huron, label="AA-00", geom=polygonA, lake_management_unit_type=huron_mu2
    )
    huron_aa.save()

    erie_aa = ManagementUnitFactory(
        lake=erie, label="AA-00", geom=polygonA, lake_management_unit_type=erie_mu
    )
    erie_aa.save()

    return [huron_qma, huron_aa, erie_aa]


@pytest.mark.django_db
def test_management_unit_api_detail(client, polygonA):
    """the api endpoint for a single management unit should return label,
    mu-type, slug, lake, centroid, and envelope.

    """

    centroid = polygonA.centroid
    lake = LakeFactory(abbrev="HU", lake_name="Lake Huron")

    qma = ManagementUnitTypeFactory(label="Quota Management Area", abbrev="QMA")

    huron_qma = LakeManagementUnitTypeFactory(lake=lake, management_unit_type=qma)

    mu = ManagementUnit(
        lake=lake, geom=polygonA, label="QMA-00", lake_management_unit_type=huron_qma
    )
    mu.save()

    url = reverse("common_api:management_unit-detail", kwargs={"slug": mu.slug})

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected_keys = [
        "id",
        "lake_abbrev",
        "label",
        "mu_type",
        "mu_type_slug",
        "slug",
        "centroid",
        "envelope",
    ]

    for key in expected_keys:
        assert key in response.data.keys()

    observed = response.data

    assert observed["slug"] == "hu_qma_qma-00"
    assert observed["centroid"] == centroid
    # assert observed["envelope"] == str(polygonA)
    assert observed["lake_abbrev"] == "HU"

    assert observed["mu_type"] == "Quota Management Area"
    assert observed["mu_type_slug"] == "qma"


@pytest.mark.django_db
def test_management_unit_api_list(client, manUnitList):
    """The endpoint for all managemnet units should return all of our
    management units, each of which should contain label, mu-type, slug,
    lake, centroid, and envelope.

    """

    url = reverse("common_api:management_unit-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == len(manUnitList)

    for obj in manUnitList:
        obj_dict = {
            "id": obj.id,
            "lake_abbrev": obj.lake.abbrev,
            "label": obj.label,
            "mu_type": obj.lake_management_unit_type.management_unit_type.label,
            "mu_type_slug": obj.lake_management_unit_type.management_unit_type.slug,
            "slug": obj.slug,
            "centroid": "SRID=4326;" + obj.centroid.wkt,
            "envelope": "SRID=4326;" + obj.envelope.wkt,
        }
        assert obj_dict in results


@pytest.mark.django_db
def test_management_unit_list_lake_filter(client, manUnitList):
    """The managemnent unit endpoint accepts a filter for lake - if a
    lake abbreviation is submitted, only management units from that
    lake should be returned.

    """

    url = reverse("common_api:management_unit-list")

    response = client.get(url, {"lake": "HU"})
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == 2

    for obj in manUnitList[:2]:
        obj_dict = {
            "id": obj.id,
            "lake_abbrev": obj.lake.abbrev,
            "label": obj.label,
            "mu_type": obj.lake_management_unit_type.management_unit_type.label,
            "mu_type_slug": obj.lake_management_unit_type.management_unit_type.slug,
            "slug": obj.slug,
            "centroid": "SRID=4326;" + obj.centroid.wkt,
            "envelope": "SRID=4326;" + obj.envelope.wkt,
        }

        assert obj_dict in results


@pytest.mark.django_db
def test_management_unit_list_mu_type_filter(client, manUnitList):
    """
    The managemnent unit endpoint accepts a filter for management unit type - if a
    management unit type is specified in the url, only management units from that
    type should be returned.
    """

    url = reverse("common_api:management_unit-list")

    response = client.get(url, {"mu_type": "aa"})
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == 2

    for obj in manUnitList[1:]:
        obj_dict = {
            "id": obj.id,
            "lake_abbrev": obj.lake.abbrev,
            "label": obj.label,
            "mu_type": obj.lake_management_unit_type.management_unit_type.label,
            "mu_type_slug": obj.lake_management_unit_type.management_unit_type.slug,
            "slug": obj.slug,
            "centroid": "SRID=4326;" + obj.centroid.wkt,
            "envelope": "SRID=4326;" + obj.envelope.wkt,
        }
        assert obj_dict in results
