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
from common.tests.common_factories import LakeManagementUnitTypeFactory
from django_filters import rest_framework as filters

from ..models import Grid5, Lake, LakeManagementUnitType, ManagementUnit, Species


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class LakeFilter(filters.FilterSet):
    """Lake objects.  We want to be able to filter them
    by lake abbreviation (e.g. ?lake=HU)"""

    lake = ValueInFilter(field_name="abbrev", lookup_expr="in")

    class Meta:
        model = Lake
        fields = ["abbrev"]


class LakeManagementUnitTypeFilter(filters.FilterSet):
    """Lake objects.  We want to be able to filter them
    by lake abbreviation (e.g. ?lake=HU)"""

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")
    mu_type = ValueInFilter(field_name="management_unit_type__slug", lookup_expr="in")

    is_primary = django_filters.BooleanFilter(field_name="primary")

    class Meta:
        model = LakeManagementUnitType
        fields = ["lake__abbrev", "management_unit_type__abbrev", "primary"]


class ManagementUnitFilter(filters.FilterSet):
    """Management Unit objects.  We want to be able to filter them
    by lake abbreviation (e.g. ?lake=HU) and type (?mu_type="ltrz")"""

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")
    mu_type = ValueInFilter(
        field_name="lake_management_unit_type__management_unit_type__slug",
        lookup_expr="in",
    )

    # primary

    class Meta:
        model = ManagementUnit
        fields = [
            "lake",
        ]


class Grid5Filter(filters.FilterSet):
    """Grid5 objects.  We want to be able to filter them
    by lake abbreviation (e.g. ?lake=HU)"""

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")

    class Meta:
        model = Grid5
        fields = ["lake"]


class SpeciesFilter(django_filters.FilterSet):

    spc = ValueInFilter(field_name="spc")
    spc__not = ValueInFilter(field_name="spc", exclude=True)

    spc_nmco__like = django_filters.CharFilter(
        field_name="spc_nmco", lookup_expr="icontains"
    )

    spc_nmsc__like = django_filters.CharFilter(
        field_name="spc_nmsc", lookup_expr="icontains"
    )

    spc_nmco__not_like = django_filters.CharFilter(
        field_name="spc_nmco", lookup_expr="icontains", exclude=True
    )

    spc_nmsc__not_like = django_filters.CharFilter(
        field_name="spc_nmsc", lookup_expr="icontains", exclude=True
    )

    class Meta:
        model = Species
        fields = ["spc", "spc_nmco", "spc_nmsc"]
