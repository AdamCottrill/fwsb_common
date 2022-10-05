"""The tests in this file ensure that the api endpoint for bottom
type work as expected and return the appropriate values.


By default the api list view should only return active records, but if
the query parameter all=T is passed in, then obsolete records should
be return too.

A single bottom type object should have the keys:

    + id
    + abbrev
    + label
    + description
    + slug
    + is_active

"""

from datetime import datetime, timezone

import pytest
from django.urls import reverse
from rest_framework import status

from ..common_factories import BottomTypeFactory


@pytest.fixture
def bottom_types():

    item1 = BottomTypeFactory(abbrev="BO", label="Boulder", description="Big rocks.")
    item2 = BottomTypeFactory(abbrev="BR", label="Bedrock or Rock")

    item3 = BottomTypeFactory(
        abbrev="CL", label="Clay", obsolete_date=datetime.now(timezone.utc).astimezone()
    )

    return [item1, item2, item3]


@pytest.mark.django_db
def test_bottom_list_default(client, bottom_types):
    """If we hit our api endpoint for bottom types, we should only
    recieve those endpoints that are currenly active (those will an
    empyt obsolete date)."""

    url = reverse("common_api:bottom-type-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 2

    expected = {x.abbrev for x in bottom_types if not x.obsolete_date}
    observed = {x["abbrev"] for x in response.data}

    assert observed == expected


@pytest.mark.django_db
def test_bottom_list_active_true(client, bottom_types):
    """If we pass the query string arguement all=True to our endpoint,
    we should get all of our values, not just those that are currently
    active."""

    url = reverse("common_api:bottom-type-list")

    response = client.get(url, {"all": True})
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 3

    expected = {x.abbrev for x in bottom_types}
    observed = {x["abbrev"] for x in response.data}

    assert observed == expected


@pytest.mark.django_db
def test_bottom_list_expected_attributes(client, bottom_types):
    """Verify that the elements returned by our bottom type endpoint
    return objects with the expected keys and that the values match
    the expected attributes."""

    url = reverse("common_api:bottom-type-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected_keys = ["id", "abbrev", "label", "description", "slug", "is_active"]
    for key in expected_keys:
        assert key in response.data[0].keys()

    observed = response.data[0]
    expected = bottom_types[0]

    assert observed["abbrev"] == expected.abbrev
    assert observed["label"] == expected.label
    assert observed["slug"] == expected.slug
    assert observed["description"] == expected.description
    assert observed["is_active"] == expected.is_active
