from datetime import datetime, timezone

import pytest
from django.utils.text import slugify

from ..models import CoverType
from .common_factories import CoverTypeFactory


@pytest.mark.django_db
def test_cover_type_str():
    """As a lookup field, cover type should be represented as a string
    a its label followed by its abbreviation in paranetheses.

    """

    abbrev = "B1"
    label = "Boulder"

    covertype = CoverTypeFactory(abbrev=abbrev, label=label)

    assert str(covertype) == f"{label}({abbrev})"


@pytest.mark.django_db
def test_cover_type_save():
    """The save method of cover type (as a lookup-table) will include
    a call to slugify which will create a slugified version of the
    label and abbreviation."""

    abbrev = "B1"
    label = "Boulder"

    covertype = CoverTypeFactory(abbrev=abbrev, label=label)
    covertype.save()
    assert covertype.slug == slugify(f"{label}-{abbrev}")


@pytest.mark.django_db
def test_cover_type_is_active():
    """the is_active property should return true if the obsolete data
    is populated, false if it is empty (None)"""

    abbrev = "B1"
    label = "Boulder"

    covertype = CoverTypeFactory(abbrev=abbrev, label=label, obsolete_date=None)

    assert covertype.is_active is True


@pytest.mark.django_db
def test_cover_type_depreciate():
    """The deactivate method of our lookup field should populate the
    obsolete date field, with th current date and time.  It shouldn't
    have any effect if is called again.

    """

    abbrev = "B1"
    label = "Boulder"

    covertype = CoverTypeFactory(abbrev=abbrev, label=label, obsolete_date=None)

    assert covertype.is_active is True
    covertype.depreciate()
    assert covertype.is_active is False
    covertype.depreciate()
    assert covertype.is_active is False


@pytest.mark.django_db
def test_cover_type_reactivate():
    """The reactivate method of our lookup field should populate
    remove any value in the obsolete_date field.  It shouldn't have
    any effect if is called again.

    """

    abbrev = "B1"
    label = "Boulder"

    covertype = CoverTypeFactory(
        abbrev=abbrev,
        label=label,
        obsolete_date=datetime.now(timezone.utc).astimezone(),
    )

    assert covertype.is_active is False
    covertype.reactivate()
    assert covertype.is_active is True
    covertype.reactivate()
    assert covertype.is_active is True


@pytest.mark.django_db
def test_cover_type_model_manager():
    """The cover type model has a custom model manager that only
    returns values that have nothing in their obsolete date field.
    All objects Including both active and obsolete objects can be
    returned using 'all_objects.'

    """

    attrs = [
        dict(
            abbrev="B1",
            label="Boulder",
            obsolete_date=datetime.now(timezone.utc).astimezone(),
        ),
        dict(abbrev="MA", label="Macrophytes", obsolete_date=None),
    ]

    for attr in attrs:
        CoverTypeFactory(**attr)

    default = CoverType.objects.all()
    assert len(default) == 1

    assert "MA" in [x.abbrev for x in default]
    assert "B1" not in [x.abbrev for x in default]

    all_objects = CoverType.all_objects.all()
    assert len(all_objects) == 2
    assert "B1" in [x.abbrev for x in all_objects]
    assert "MA" in [x.abbrev for x in all_objects]
