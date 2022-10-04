import pytest
from django.urls import reverse
from rest_framework import status

from ..fixtures import taxon_list


@pytest.mark.django_db
def test_taxon_api_detail_keys_values(client, taxon_list):

    """Verify that the elements returned by our bottom type endpoint
    return objects with the expected keys and that the values match
    the expected attributes."""

    taxa = taxon_list[0]

    url = reverse("common_api:taxon-list")

    response = client.get(url, {"taxon": taxa.taxon})
    assert response.status_code == status.HTTP_200_OK

    observed = response.data["results"][0]

    expected_keys = [
        "taxon",
        "itiscode",
        "taxon_name",
        "taxon_label",
        "taxonomic_rank",
        "vertinvert",
        "omnr_provincial_code",
    ]
    for key in expected_keys:
        assert key in observed.keys()

    assert observed["taxon"] == taxa.taxon
    assert observed["itiscode"] == taxa.itiscode
    assert observed["taxon_name"] == taxa.taxon_name
    assert observed["taxon_label"] == taxa.taxon_label
    assert observed["taxonomic_rank"] == taxa.taxonomic_rank
    assert observed["vertinvert"] == taxa.vertinvert
    assert observed["omnr_provincial_code"] == taxa.omnr_provincial_code


@pytest.mark.django_db
def test_taxon_api_list(client, taxon_list):
    """the taxon api endpoint should return all of our taxon items."""

    url = reverse("common_api:taxon-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    observed = {x["omnr_provincial_code"] for x in response.data["results"]}
    expected = {x.omnr_provincial_code for x in taxon_list}

    assert expected == observed


@pytest.mark.django_db
def test_taxon_filter_taxon_node(client, taxon_list):
    """The taxon api has a filter for taxon node that should return
    that taxon an deverthing below it.

    """
    # using the itis code for oncorhynchus genus:
    taxon_node = "161974"
    url = reverse("common_api:taxon-list")

    response = client.get(url, {"taxon_node": "161974"})
    assert response.status_code == status.HTTP_200_OK

    observed = {x["omnr_provincial_code"] for x in response.data["results"]}

    expected = {"075", "076", "084"}

    assert expected == observed
