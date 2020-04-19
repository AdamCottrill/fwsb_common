"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/uglmu_common/common/api/filters.py
 Created: 17 Apr 2020 08:46:55


 DESCRIPTION:

Filterset classes used by our api view to select specific subsets of
records.

 A. Cottrill
=============================================================

"""


import django_filters
from django_filters import rest_framework as filters

from ..models import Grid5, ManagementUnit


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class Grid5Filter(filters.FilterSet):
    """Grid5 objects.  We want to be able to filter them
    by lake abbreviation (e.g. ?lake=HU)"""

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")

    class Meta:
        model = Grid5
        fields = ["lake"]


class ManagementUnitFilter(filters.FilterSet):
    """Management Unit objects.  We want to be able to filter them
    by lake abbreviation (e.g. ?lake=HU) and type (?mu_type="ltrz")"""

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")
    mu_type = ValueInFilter(field_name="mu_type", lookup_expr="in")

    class Meta:
        model = ManagementUnit
        fields = ["lake", "mu_type"]
