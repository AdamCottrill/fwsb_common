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


@pytest.mark.django_db
def test_species_api_detail(client):
    """ The species detail endpoint should include: species name, species code,
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
def test_species_api_list(client):
    """Species list should return all species objects, but only the basic
    fields - species code, common name, and scientific name.

    """

    objects = [
        {
            "spc": "091",
            "spc_nmco": "lake whitefish",
            "spc_nmsc": "Coregonus clupeaformis",
        },
        {"spc": "331", "spc_nmco": "Yellow Perch", "spc_nmsc": "Perca flavescens"},
        {"spc": "334", "spc_nmco": "walleye", "spc_nmsc": "Sander vitreum"},
    ]

    for obj in objects:
        SpeciesFactory(**obj)

    url = reverse("common_api:species-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(objects)

    for obj in objects:
        assert obj in response.data
