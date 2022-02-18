"""=============================================================
~/uglmu_common/common/tests/api/test_species.py
 Created: 18 Apr 2020 09:26:31

 DESCRIPTION:

  Tests for the api end points for Species

  Species detail should include: species name, species code,
  scientific name, label and abbreviation.

  Species list should return all species objects.  It does not
  currently have any filters (or many fields to filter on), but fields
  for commerical fish and/or sport fish could be added.

 A. Cottrill
=============================================================

"""

import pytest

from django.urls import reverse
from rest_framework import status

from ..common_factories import SpeciesFactory
from ..fixtures import species_list


@pytest.mark.django_db
def test_species_api_detail(client):
    """The species detail endpoint should include: species name, species code,
    scientific name, label and US abbreviation.
    """

    attrs = {
        "spc": "091",
        "abbrev": "LWF",
        "spc_nmco": "lake whitefish",
        "spc_nmsc": "Coregonus clupeaformis",
        "spc_nmfam": "COREGONINAE",
        "spc_lab": "LaWhi",
    }

    species = SpeciesFactory(**attrs)

    url = reverse("common_api:species-detail", kwargs={"spc": species.spc})

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert attrs == response.data


@pytest.mark.django_db
def test_species_api_list(client, species_list):
    """Species list should return all species objects, but only the basic
    fields - species code, common name, and scientific name.

    """

    url = reverse("common_api:species-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(species_list)

    for item in species_list:
        obj = {"spc": item.spc, "spc_nmco": item.spc_nmco, "spc_nmsc": item.spc_nmsc}
        assert obj in response.data


filter_args = [
    ({"spc": "091"}, ["091"]),
    ({"spc": "331,334"}, ["331", "334"]),
    ({"spc__not": "091"}, ["331", "334"]),
    ({"spc__not": "331,334"}, ["091"]),
    ({"spc_nmco__like": "ye"}, ["331", "334"]),
    ({"spc_nmco__not_like": "ye"}, ["091"]),
    ({"spc_nmsc__like": "er"}, ["331", "334"]),
    ({"spc_nmsc__not_like": "er"}, ["091"]),
]


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_species_api_filter(client, species_list, filter, expected):
    """Species list endpoint has filters that work on spc, common name and
    scientific name.  Verify that they work as expected.

    """

    url = reverse("common_api:species-list")

    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    observed = [x["spc"] for x in response.data]

    assert set(observed) == set(expected)


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_species_flen2tlen_filter(client, species_list, filter, expected):
    """Verify that the flen2tlen endpoint respects the same filters as the
    species list

    """

    url = reverse("common_api:flen2tlen-list")

    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    observed = [x["spc"] for x in response.data]

    assert set(observed) == set(expected)


@pytest.mark.django_db
def test_species_flen2tlen_detail(client, species_list):
    """Verify that the flen2tlen endpoint has the fields we exect it to have"""

    url = reverse("common_api:flen2tlen-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {"spc", "intercept", "slope"}
    first = response.data[0]
    observed = set([key for key in first.keys()])

    assert observed == expected
