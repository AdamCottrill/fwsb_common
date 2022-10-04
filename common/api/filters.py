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

from ..models import Grid5, Lake, LakeManagementUnitType, ManagementUnit, Species, Taxon


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
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


def taxon_node_filter(queryset, name, value):
    """A custom query method to return all of the values from a node
    and its children.

    Arguments:

    - `queryset`: A queryset that can be related directly or through
      joins to itis_taxon.Taxon model

    - `name`: string represtenting relationship from current model to
       itis_taxon.Taxon model.  Expects django's "__" conventions

    - `value`: the taxon value (itis code or HHFAU code) associated
      with the target node.

    """

    if not value:
        return queryset

    taxon = Taxon.objects.filter(taxon=value).first()

    if taxon:
        descendants = [x[0] for x in taxon.get_descendants().values_list("taxon")]
        descendants.append(taxon.taxon)

        queryset = queryset.filter(**{"%s__in" % name: descendants}).order_by("path")

    return queryset


class TaxonFilter(django_filters.FilterSet):

    # "taxon",
    taxon = ValueInFilter(field_name="taxon")

    taxon__node = django_filters.CharFilter(
        field_name="taxon", method=taxon_node_filter
    )

    # "itiscode",
    # exact
    itiscode = NumberInFilter(field_name="itiscode")

    # "taxon_name",
    taxon_name = django_filters.CharFilter(field_name="taxon_name", lookup_expr="exact")
    taxon_name__like = django_filters.CharFilter(
        field_name="taxon_name", lookup_expr="icontains"
    )

    # "taxon_label",
    taxon_label = django_filters.CharFilter(
        field_name="taxon_label", lookup_expr="exact"
    )
    taxon_label__like = django_filters.CharFilter(
        field_name="taxon_label", lookup_expr="icontains"
    )

    # "taxonomic_rank",
    taxonomic_rank = ValueInFilter(field_name="taxonomic_rank")

    # "vertinvert",
    vertinvert = ValueInFilter(field_name="vertinvert")

    # "omnr_provincial_code",
    hhfau = ValueInFilter(field_name="omnr_provincial_code")

    class Meta:
        model = Taxon
        fields = [
            "taxon",
            "itiscode",
            "taxon_name",
            "taxon_label",
            "taxonomic_rank",
            "vertinvert",
            "omnr_provincial_code",
        ]
