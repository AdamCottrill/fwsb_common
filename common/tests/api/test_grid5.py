"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/uglmu_common/common/tests/api/test_grid5.py
 Created: 18 Apr 2020 09:13:43


 DESCRIPTION:

  Tests for the api end points for Grid5 objects

  Grid detail should include: grid number, lake, centroid, envelope,


  Grid list should return all grid objects and accept filters for one
  or more lakes

 A. Cottrill
=============================================================

"""

import pytest
from django.contrib.gis.geos import GEOSGeometry
from django.urls import reverse
from rest_framework import status

from common.models import Grid5
from ..common_factories import LakeFactory


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
def polygonB():
    """A polygon somewhere in Lake Superior."""

    wkt = (
        "MULTIPOLYGON(((-87.0 48.0,"
        + "-87.5 48.0,"
        + "-87.5 48.5,"
        + "-87.0 48.5,"
        + "-87.0 48.0)))"
    )
    return GEOSGeometry(wkt.replace("\n", ""), srid=4326)


@pytest.fixture()
def polygonC():
    """A polygon somewhere in Lake Erie."""

    wkt = (
        "MULTIPOLYGON(((-81.0 42.0,"
        + "-81.5 42.0,"
        + "-81.5 42.5,"
        + "-81.0 42.5,"
        + "-81.0 42.0)))"
    )
    return GEOSGeometry(wkt.replace("\n", ""), srid=4326)


@pytest.fixture()
def gridList(polygonA, polygonB, polygonC):
    """a List of 5-minute grid objects - one from each lake."""

    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
    grid_huron = Grid5(lake=huron, grid="111", geom=polygonA)
    grid_huron.save()

    erie = LakeFactory(abbrev="ER", lake_name="Lake Erie")
    grid_erie = Grid5(lake=erie, grid="2222", geom=polygonB)
    grid_erie.save()

    superior = LakeFactory(abbrev="SU", lake_name="Lake Superior")
    grid_superior = Grid5(lake=superior, grid="3333", geom=polygonC)
    grid_superior.save()

    return [grid_huron, grid_erie, grid_superior]


@pytest.mark.django_db
def test_grid5_api_detail(client, polygonA):
    """Grid detail should include: grid number, lake, centroid, envelope,"""

    centroid = polygonA.centroid
    lake = LakeFactory(abbrev="HU", lake_name="Lake Huron")

    grid5 = Grid5(lake=lake, geom=polygonA, grid=1234)
    grid5.save()

    url = reverse("common_api:grid5-detail", kwargs={"slug": grid5.slug})

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected_keys = ["grid", "lake", "centroid", "envelope"]
    for key in expected_keys:
        assert key in response.data.keys()

    observed = response.data

    assert observed["slug"] == "hu_1234"
    assert observed["centroid"] == centroid
    ##assert observed["envelope"] == polygonA.wkt
    assert observed["lake"] == {"abbrev": "HU", "lake_name": "Lake Huron"}


@pytest.mark.django_db
def test_grid5_api_list(client, gridList):
    """Grid list should return all grid objects and accept filter for
    one or more lakes"""

    url = reverse("common_api:grid5-list")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == len(gridList)

    for obj in gridList:
        obj_dict = {
            "id": obj.id,
            "grid": obj.grid,
            "lake_abbrev": obj.lake.abbrev,
            "slug": obj.slug,
            "centroid": str(obj.centroid),
        }
        assert obj_dict in results


@pytest.mark.django_db
def test_grid5_api_list_filter_one_grid5(client, gridList):
    """the grid5 list with a filter a single grid5 should retun just that grid5"""

    url = reverse("common_api:grid5-list")

    response = client.get(
        url,
        {
            "lake": [
                "HU",
            ]
        },
    )
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == 1

    # extract our expected object:
    obj = gridList[0]
    obj_dict = {
        "id": obj.id,
        "grid": obj.grid,
        "lake_abbrev": obj.lake.abbrev,
        "slug": obj.slug,
        "centroid": str(obj.centroid),
    }

    assert obj_dict in results


@pytest.mark.django_db
def test_grid5_api_list_filter_two_grid5s(client, gridList):
    """the grid5 list with a filter for two grid5s should return those those
    two grid5s, not the third.

    """

    url = reverse("common_api:grid5-list")

    response = client.get(url, {"lake": ["HU, ER"]})
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == 2

    for obj in gridList[:2]:
        obj_dict = {
            "id": obj.id,
            "grid": obj.grid,
            "lake_abbrev": obj.lake.abbrev,
            "slug": obj.slug,
            "centroid": str(obj.centroid),
        }

        assert obj_dict in results
