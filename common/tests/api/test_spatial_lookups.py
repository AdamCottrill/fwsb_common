"""=============================================================
~/uglmu_common/common/tests/api/test_spatial_lookups.py
 Created: 19 Apr 2020 09:47:38

 DESCRIPTION:

  The spatial lookup api endpoints accept a lat-lon coordinate and
  return the attributes of the object that contains that point within
  its geometry.  There are spatial lookup end points for:

  + lakes
  + management units
  + 5-minute grids


 A. Cottrill
=============================================================

"""
import pytest
from django.contrib.gis.geos import GEOSGeometry
from django.urls import reverse
from rest_framework import status
from ..common_factories import LakeFactory, ManagementUnitFactory, Grid5Factory


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
def polygonB():
    """A polygon somewhere in Lake Superior
    """
    wkt = (
        "MULTIPOLYGON(((-87.0 48.0,"
        + "-87.5 48.0,"
        + "-87.5 48.5,"
        + "-87.0 48.5,"
        + "-87.0 48.0)))"
    )
    return GEOSGeometry(wkt.replace("\n", ""), srid=4326)


@pytest.mark.django_db
def test_get_spatial_attributes(client, polygonA):
    """If we pass coordinates to our spatial attributes endpoint, we
    should recieve a dictionary with the keys lake, jurisdiction,
    manUnit, and grid5.  Each element of those keys, should also be a
    dictionary with the basic information of the geometries derived
    from ddlat and ddlon.

    This endpoint is intended to serve form validation, so it only
    returns the attributes (and management unit types) included in
    those forms.

    """

    # get a point inside our polygon we wil use to select our geometries
    centroid = polygonA.centroid

    assert polygonA.contains(centroid) is True

    # create a lake, jurisdiciton, management_unit and a grid (they all
    # share the same polygon, but that doesn't matter here)
    huron = dict(abbrev="HU", lake_name="Lake Huron", geom=polygonA)
    huron_obj = LakeFactory(**huron)

    ManagementUnitFactory(
        label="OH-3", lake=huron_obj, geom=polygonA, mu_type="stat_dist"
    )

    Grid5Factory(grid=1234, lake=huron_obj, geom=polygonA)

    url = reverse("common_api:api-lookup-spatial-attrs")

    response = client.post(url, {"point": centroid.wkt})
    assert response.status_code == status.HTTP_200_OK

    expected_keys = ["lake", "manUnit", "grid5"]
    for key in expected_keys:
        assert key in response.data.keys()

    # verify that we got thte right objects back:

    observed = response.data.get("lake")
    assert observed != ""
    assert observed.get("abbrev") == "HU"
    assert observed.get("lake_name") == "Lake Huron"

    observed = response.data.get("manUnit")
    assert observed != ""
    assert observed.get("slug") == "hu_stat_dist_oh-3"
    assert observed.get("label") == "OH-3"

    observed = response.data.get("grid5")
    assert observed != ""
    assert observed.get("grid") == "1234"
    assert observed.get("lake_abbrev") == "HU"
    assert observed.get("slug") == "hu_1234"


@pytest.mark.django_db
def test_get_spatial_attributes_empty(client, polygonA, polygonB):
    """If we pass coordinates to our spatial attributes endpoint that fall
    OUTSIDE of any the geometry, we should recieve a dictionary with
    keys lake, manUnit, and grid5, but elements of each
    key will be an empty string.

    """

    # get a point outside of the polygon we will use to build our data elements
    centroid = polygonB.centroid

    assert polygonA.contains(centroid) is False

    # create a lake, jurisdiciton, management_unit and a grid (they all
    # share the same polygon, but that doesn't matter here)
    huron = dict(abbrev="HU", lake_name="Lake Huron", geom=polygonA)
    huron_obj = LakeFactory(**huron)

    ManagementUnitFactory(
        label="OH-3", lake=huron_obj, geom=polygonA, mu_type="stat_dist"
    )

    Grid5Factory(grid=1234, lake=huron_obj, geom=polygonA)

    url = reverse("common_api:api-lookup-spatial-attrs")

    response = client.post(url, {"point": centroid.wkt})
    assert response.status_code == status.HTTP_200_OK

    expected_keys = ["lake", "manUnit", "grid5"]
    for key in expected_keys:
        assert key in response.data.keys()

    # verify that we got thte right objects back:

    observed = response.data.get("lake")
    assert observed == ""

    observed = response.data.get("manUnit")
    assert observed == ""

    observed = response.data.get("grid5")
    assert observed == ""


@pytest.mark.django_db
def test_get_lake_from_point(client, polygonA, polygonB):
    """If we pass coordinates to our endpoint that fall within the geometry
    of a lake object, we should get a response back that contains the
    details of that lake object.

    """
    # create two lakes with disjoint geometries - the first geom will
    # contain our point:

    # get a point inside our polygon we wil use to select it
    centroid = polygonA.centroid

    assert polygonA.contains(centroid) is True

    huron = dict(abbrev="HU", lake_name="Lake Huron", geom=polygonA)
    huron = LakeFactory(**huron)
    huron.save()

    superior = dict(abbrev="SU", lake_name="Lake Superior", geom=polygonA)
    LakeFactory(**superior)

    url = reverse("common_api:api-lookup-lake-from-pt")

    response = client.post(url, {"point": centroid.wkt})
    assert response.status_code == status.HTTP_200_OK

    expected_keys = [
        "abbrev",
        "centroid",
        "envelope",
        "centroid_ontario",
        "envelope_ontario",
        "id",
        "lake_name",
    ]
    for key in expected_keys:
        assert key in response.data.keys()

    # verify that we got thte right object
    assert response.data.get("abbrev") == "HU"
    assert response.data.get("lake_name") == "Lake Huron"


@pytest.mark.django_db
def test_get_lake_from_point_400(client):
    """If we pass bad coordinates to our lake lookup endpoint, should
    return a reponse with status 400

    """
    url = reverse("common_api:api-lookup-lake-from-pt")
    response = client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_lake_from_point_404(client, polygonA, polygonB):
    """If we pass coordinates to our lake lookup endpoint, that are
    outside of any existing polygon, we return a reponse with status 404

    """
    # get a point outside our polygon
    centroid = polygonB.centroid
    assert polygonA.contains(centroid) is False

    huron = dict(abbrev="HU", lake_name="Lake Huron", geom=polygonA)
    LakeFactory(**huron)

    url = reverse("common_api:api-lookup-lake-from-pt")
    response = client.post(url, {"point": centroid.wkt})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_manUnit_from_point_pure_wo_param(client, polygonA, polygonB):
    """If we pass coordinates to our management spatial lookup endpoint
    and do not provide any query parameters, we should get the default
    management area that has default=True.
    """

    # get a point inside our polygon we wil use to select it
    centroid = polygonA.centroid

    assert polygonA.contains(centroid) is True

    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")

    ManagementUnitFactory(
        label="OH-1", lake=huron, geom=polygonA, primary=True, mu_type="stat_dist"
    )
    ManagementUnitFactory(
        label="OH-2", lake=huron, geom=polygonB, primary=True, mu_type="stat_dist"
    )

    # same geometry as OH-1, different mu type and primary designation:
    ManagementUnitFactory(
        label="QMA-1", lake=huron, geom=polygonA, primary=False, mu_type="qma"
    )

    url = reverse("common_api:api-lookup-management-unit-from-pt")

    response = client.post(url, {"point": centroid.wkt})
    assert response.status_code == status.HTTP_200_OK

    expected_keys = ["id", "slug", "label", "mu_type", "centroid", "envelope"]

    for key in expected_keys:
        assert key in response.data.keys()

    # verify that we got thte right object
    assert response.data.get("label") == "OH-1"


@pytest.mark.django_db
def test_get_manUnit_from_point_pure_w_param(client, polygonA, polygonB):
    """If we pass coordinates to our management spatial lookup endpoint
    and with a mu_type parameter, we should get the management unit
    of that type (not necessarily the  default mu_type).

    """

    # get a point inside our polygon we wil use to select it
    centroid = polygonA.centroid
    assert polygonA.contains(centroid) is True

    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
    ManagementUnitFactory(label="OH-1", lake=huron, geom=polygonA, mu_type="stat_dist")
    ManagementUnitFactory(label="OH-2", lake=huron, geom=polygonB, mu_type="stat_dist")

    # same geometry, different mu type and primary designation.  This
    # is the one we should get back:
    ManagementUnitFactory(
        label="QMA-1", lake=huron, geom=polygonA, primary=False, mu_type="qma"
    )

    url = reverse("common_api:api-lookup-management-unit-from-pt")

    response = client.post(url + "?mu_type=qma", {"point": centroid.wkt})
    assert response.status_code == status.HTTP_200_OK

    expected_keys = ["id", "slug", "label", "mu_type", "centroid", "envelope"]

    for key in expected_keys:
        assert key in response.data.keys()

    # verify that we got thte right object
    assert response.data.get("label") == "QMA-1"


@pytest.mark.django_db
def test_get_manUnit_from_point_pure_w_all(client, polygonA, polygonB):
    """If we pass coordinates to our management spatial lookup endpoint
    and with parameter all=True, we should get a list of the json objects
    representing all of the management units that contains that point.
    """

    # get a point inside our polygon we wil use to select it
    centroid = polygonA.centroid

    assert polygonA.contains(centroid) is True

    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")

    ManagementUnitFactory(label="OH-1", lake=huron, geom=polygonA)
    ManagementUnitFactory(label="OH-2", lake=huron, geom=polygonB)

    # same geometry, different mu type and primary designation:
    ManagementUnitFactory(
        label="QMA-1", lake=huron, geom=polygonA, primary=False, mu_type="qma"
    )

    url = reverse("common_api:api-lookup-management-unit-from-pt")

    response = client.post(url + "?all=True", {"point": centroid.wkt})
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 2

    expected = ["QMA-1", "OH-1"]
    observed = [x.get("label") for x in response.data]

    expected.sort()
    observed.sort()

    # verify that we got thte right object
    assert expected == observed


@pytest.mark.django_db
def test_get_management_unit_from_point_400(client):
    """If we pass bad coordinates to our management unit lookup endpoint, should
    return a reponse with status 400

    """
    url = reverse("common_api:api-lookup-management-unit-from-pt")
    response = client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_management_unit_from_point_404(client, polygonA, polygonB):
    """If we pass coordinates to our management_unit lookup endpoint, that are
    outside of any existing polygon, we return a reponse with status 404

    """
    # get a point outside our polygon and verify that this is the case
    centroid = polygonB.centroid
    assert polygonA.contains(centroid) is False

    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
    ManagementUnitFactory(label="OH-1", lake=huron, geom=polygonA)

    url = reverse("common_api:api-lookup-management-unit-from-pt")
    response = client.post(url, {"point": centroid.wkt})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_grid5_from_point_pure(client, polygonA, polygonB):
    """If we pass coordinates to our grid5 spatial lookup endpoint that
    fall within the geometry of a grid5 object, we should get a
    response back that contains the details of that grid5 object.

    """

    # get a point inside our polygon we wil use to select it
    centroid = polygonA.centroid

    assert polygonA.contains(centroid) is True

    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")

    Grid5Factory(grid=1234, lake=huron, geom=polygonA)
    Grid5Factory(grid=5678, lake=huron, geom=polygonB)

    url = reverse("common_api:api-lookup-grid5-from-pt")

    response = client.post(url, {"point": centroid.wkt})
    assert response.status_code == status.HTTP_200_OK

    expected_keys = ["id", "grid", "centroid", "envelope", "lake"]

    for key in expected_keys:
        assert key in response.data.keys()

    # verify that we got thte right object
    assert response.data.get("grid") == "1234"
    assert response.data.get("slug") == "hu_1234"
    assert response.data.get("lake") == dict(
        lake_name="Lake Huron", lake_id=huron.id, lake_abbrev="HU"
    )


@pytest.mark.django_db
def test_get_grid5_from_point_400(client):
    """If we pass bad coordinates to our grid lookup endpoint, should
    return a reponse with status 400

    """
    url = reverse("common_api:api-lookup-grid5-from-pt")
    response = client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_grid5_from_point_404(client, polygonA, polygonB):
    """If we pass coordinates to our grid5 lookup endpoint, that are
    outside of any existing polygon, we return a reponse with status 404

    """
    # get a point outside our polygon and verify that this is the case
    centroid = polygonB.centroid
    assert polygonA.contains(centroid) is False

    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
    Grid5Factory(grid=1234, lake=huron, geom=polygonA)

    url = reverse("common_api:api-lookup-grid5-from-pt")
    response = client.post(url, {"point": centroid.wkt})
    assert response.status_code == status.HTTP_404_NOT_FOUND
