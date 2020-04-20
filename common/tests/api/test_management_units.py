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

from django.contrib.gis.geos import GEOSGeometry
from django.urls import reverse
from rest_framework import status

from common.models import ManagementUnit
from ..common_factories import LakeFactory


@pytest.fixture()
def polygonA():
    """A polygon somewhere in Lake Huron.
    """

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

    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
    huron_qma = ManagementUnit(lake=huron, label="QMA-00", geom=polygonA, mu_type="qma")
    huron_qma.save()

    huron_aa = ManagementUnit(lake=huron, label="AA-00", geom=polygonA, mu_type="aa")
    huron_aa.save()

    erie = LakeFactory(abbrev="ER", lake_name="Lake Erie")
    erie_aa = ManagementUnit(lake=erie, label="AA-00", geom=polygonA, mu_type="aa")
    erie_aa.save()

    return [huron_qma, huron_aa, erie_aa]


@pytest.mark.django_db
def test_management_unit_api_detail(client, polygonA):
    """the api endpoint for a single management unit should return label,
  mu-type, slug, lake, centroid, and envelope.

    """

    centroid = polygonA.centroid
    lake = LakeFactory(abbrev="HU", lake_name="Lake Huron")

    mu = ManagementUnit(lake=lake, geom=polygonA, label="QMA-00")
    mu.save()

    url = reverse("common_api:management_unit-detail", kwargs={"slug": mu.slug})

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected_keys = ["label", "slug", "lake", "centroid", "envelope"]
    for key in expected_keys:
        assert key in response.data.keys()

    observed = response.data

    assert observed["slug"] == "hu_mu_qma-00"
    assert observed["centroid"] == centroid
    ##assert observed["envelope"] == polygonA.wkt
    assert observed["lake"] == {"abbrev": "HU", "lake_name": "Lake Huron"}


@pytest.mark.django_db
def test_management_unit_api_list(client, manUnitList):
    """The endpoint for all managemnet units should return all of our
    management units, each of which should contain label, mu-type, slug,
    lake, centroid, and envelope.

    """

    url = reverse("common_api:management_unit-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(manUnitList)

    observed = response.data

    for obj in manUnitList:
        obj_dict = {
            "label": obj.label,
            "slug": obj.slug,
            "lake": dict(abbrev=obj.lake.abbrev, lake_name=obj.lake.lake_name),
            "mu_type": obj.mu_type,
            "centroid": "SRID=4326;" + obj.centroid.wkt,
            "envelope": "SRID=4326;" + obj.envelope.wkt,
        }
        assert obj_dict in observed


@pytest.mark.django_db
def test_management_unit_list_lake_filter(client, manUnitList):
    """The managemnent unit endpoint accepts a filter for lake - if a
    lake abbreviation is submitted, only management units from that
    lake should be returned.

    """

    url = reverse("common_api:management_unit-list")

    response = client.get(url + "?lake=HU")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    observed = response.data

    for obj in manUnitList[:2]:
        obj_dict = {
            "label": obj.label,
            "slug": obj.slug,
            "lake": dict(abbrev=obj.lake.abbrev, lake_name=obj.lake.lake_name),
            "mu_type": obj.mu_type,
            "centroid": "SRID=4326;" + obj.centroid.wkt,
            "envelope": "SRID=4326;" + obj.envelope.wkt,
        }
        assert obj_dict in observed


@pytest.mark.django_db
def test_management_unit_list_mu_type_filter(client, manUnitList):
    """The managemnent unit endpoint accepts a filter for management unit type - if a
    management unit type is specified in the url, only management units from that
    type should be returned.
    """

    url = reverse("common_api:management_unit-list")

    response = client.get(url + "?mu_type=aa")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    observed = response.data

    for obj in manUnitList[1:]:
        obj_dict = {
            "label": obj.label,
            "slug": obj.slug,
            "lake": dict(abbrev=obj.lake.abbrev, lake_name=obj.lake.lake_name),
            "mu_type": obj.mu_type,
            "centroid": "SRID=4326;" + obj.centroid.wkt,
            "envelope": "SRID=4326;" + obj.envelope.wkt,
        }
        assert obj_dict in observed
