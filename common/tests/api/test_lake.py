"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/uglmu_common/common/tests/api/test_lake.py
 Created: 18 Apr 2020 09:13:43


 DESCRIPTION:

  Tests for the api end points for Lake

  Lake detail should include: lake name, abbrev, centroid, envelope,
  centroid_ontario, envelope_ontario

  Lake list should return all lake objects and accept filter for one
  or more lakes.

 A. Cottrill
=============================================================

"""

import pytest
from django.contrib.gis.geos import GEOSGeometry
from django.urls import reverse
from rest_framework import status

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


@pytest.mark.django_db
def test_lake_api_detail(client, polygonA):
    """
    """

    centroid = polygonA.centroid
    lake = LakeFactory(
        abbrev="HU", lake_name="Huron", geom=polygonA, geom_ontario=polygonA
    )
    lake.save()

    url = reverse("common_api:lake-detail", kwargs={"abbrev": lake.abbrev})

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected_keys = [
        "abbrev",
        "lake_name",
        "centroid",
        "envelope",
        "centroid_ontario",
        "envelope_ontario",
    ]
    for key in expected_keys:
        assert key in response.data.keys()

    observed = response.data

    assert observed["abbrev"] == "HU"
    assert observed["lake_name"] == "Huron"
    assert observed["centroid"] == centroid
    ##assert observed["envelope"] == polygonA.wkt
    assert observed["centroid_ontario"] == centroid
    # assert observed["envelope_ontario"] == polygonA


@pytest.mark.django_db
def test_lake_api_list(client):
    """
    """

    objects = [
        dict(abbrev="HU", lake_name="Huron"),
        dict(abbrev="SU", lake_name="Superior"),
        dict(abbrev="ER", lake_name="Erie"),
    ]

    for obj in objects:
        LakeFactory(**obj)

    url = reverse("common_api:lake-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3

    for obj in objects:
        assert obj in response.data


@pytest.mark.django_db
def test_lake_api_list_filter_one_lake(client):
    """the lake list with a filter a single lake should retun just that lake
    """

    objects = [
        dict(abbrev="HU", lake_name="Huron"),
        dict(abbrev="SU", lake_name="Superior"),
        dict(abbrev="ER", lake_name="Erie"),
    ]

    for obj in objects:
        LakeFactory(**obj)

    url = reverse("common_api:lake-list")

    response = client.get(url + "?lake=HU")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

    assert objects[0] in response.data


@pytest.mark.django_db
def test_lake_api_list_filter_two_lakes(client):
    """the lake list with a filter for two lakes should return those those
    two lakes, not the third.

    """

    objects = [
        dict(abbrev="HU", lake_name="Huron"),
        dict(abbrev="SU", lake_name="Superior"),
        dict(abbrev="ER", lake_name="Erie"),
    ]

    for obj in objects:
        LakeFactory(**obj)

    url = reverse("common_api:lake-list")

    response = client.get(url + "?lake=HU,SU")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    for obj in objects[:2]:
        assert obj in response.data
