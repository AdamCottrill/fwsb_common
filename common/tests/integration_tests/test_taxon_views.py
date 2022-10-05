"""Our taxon template should render all of out taxon elements into a
table by default.  If search is supplied, it the rendered table should
only include that node and the ones below it. If no taxon are found a
meaingful message should appear.

"""
import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains, assertNotContains
from ..fixtures import taxon_list


@pytest.mark.django_db
def test_taxon_list_uses_correct_template(client, taxon_list):
    """The taxon list should be rendered using 'common/taxon_list.html'"""

    url = reverse("common:taxon_list")
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "common/taxon_list.html")


@pytest.mark.django_db
def test_taxon_table(client, taxon_list):
    """The default view for our taxon list should be a table that
    contains each of taxon elements."""

    url = reverse("common:taxon_list")
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "common/taxon_list.html")

    expected = [x.itiscode for x in taxon_list]

    for itis_code in expected:
        link = f'<td><a href="{url}?search={itis_code}">{itis_code}</a></td>'
        assertContains(response, link, html=True)


@pytest.mark.django_db
def test_taxon_table_search(client, taxon_list):
    """If we include a search term for onchoryncus, only three of
    taxon should be rendered.
    """

    url = reverse("common:taxon_list")
    response = client.get(url, {"search": "161974"})
    assert response.status_code == 200
    assertTemplateUsed(response, "common/taxon_list.html")

    spc_codes = ["075", "076", "084"]

    expected = [x.itiscode for x in taxon_list if x.omnr_provincial_code in spc_codes]

    for itis_code in expected:
        link = f'<td><a href="{url}?search={itis_code}">{itis_code}</a></td>'
        assertContains(response, link, html=True)

    not_expected = [
        x.itiscode for x in taxon_list if x.omnr_provincial_code not in spc_codes
    ]

    for itis_code in not_expected:
        link = f'<td><a href="{url}?search={itis_code}">{itis_code}</a></td>'
        assertNotContains(response, link, html=True)


@pytest.mark.django_db
def test_taxon_table_invalid_search(client, taxon_list):
    """If we include a search term for a taxon that does not exist, a
    meaninful message should be presented to the user.

    """

    search_criteria = "999999"
    url = reverse("common:taxon_list")
    response = client.get(url, {"search": search_criteria})
    assert response.status_code == 200
    assertTemplateUsed(response, "common/taxon_list.html")

    expected = f'No taxon match the criteria <em>"{search_criteria}"</em>'
    assertContains(response, expected, html=True)
