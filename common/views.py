from django.db.models import F, Q, Subquery, CharField, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Grid5, Lake, ManagementUnit, Species, Taxon


def grouped(items, ncol):
    """a little helper function that we can wrap our querysets in to
    display them as tables on our templates."""
    for i in range(0, len(items), ncol):
        yield items[i : i + ncol]


class SpeciesList(ListView):

    template_name = "common/species_list.html"
    model = Species
    queryset = Species.objects.all()


class SpeciesDetail(DetailView):

    template_name = "common/species_detail.html"
    model = Species
    slug_field = "spc"
    queryset = Species.objects.all()

    def get_object(self):
        return get_object_or_404(Species, spc=self.kwargs["spc"])


class TaxonList(ListView):

    template_name = "common/taxon_list.html"
    model = Taxon

    def get_taxon(self):
        """ """

        search = self.request.GET.get("search")

        if search:
            try:
                taxon = Taxon.objects.filter(taxon=int(search)).first()
                return taxon
            except ValueError:
                return search
        else:
            return None

    def get_queryset(self):
        """ """

        # taxon = self.get_taxon()

        search = self.request.GET.get("search")
        taxon = None
        if search:
            try:
                taxon = Taxon.objects.filter(taxon=int(search)).first()
            except ValueError:
                pass
            if taxon is None:
                return []

        if taxon:
            descendants = taxon.get_descendants()
            qs = Taxon.objects.filter(
                Q(pk__in=Subquery(descendants.values("id"))) | Q(pk=taxon.pk)
            ).order_by("path")
        else:
            qs = Taxon.objects.all().order_by("path")

        return qs

    def get_context_data(self, **kwargs):
        """
        get any additional context information that has been passed in with
        the request.
        """

        context = super(TaxonList, self).get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search")
        context["taxon"] = self.get_taxon()

        return context


class LakeList(ListView):

    template_name = "common/lake_list.html"
    model = Lake
    queryset = Lake.objects.all()


class LakeDetail(DetailView):

    template_name = "common/lake_detail.html"
    model = Lake
    slug_field = "abbrev"
    queryset = Lake.objects.all()

    def get_object(self):
        return get_object_or_404(Lake, abbrev=self.kwargs["abbrev"])

    def get_context_data(self, **kwargs):
        """Add the list of management units for this lake to our context"""
        context = super().get_context_data(**kwargs)
        mus = (
            ManagementUnit.objects.filter(lake__abbrev=self.kwargs["abbrev"])
            .prefetch_related(
                "lake_management_unit_type",
                "lake_management_unit_type__management_unit_type",
            )
            .annotate(
                primary=F("lake_management_unit_type__primary"),
                mu_type=F("lake_management_unit_type__management_unit_type__label"),
                short_name=Concat(
                    "lake_management_unit_type__management_unit_type__abbrev",
                    Value(": "),
                    "label",
                    output_field=CharField(),
                ),
            )
            .values("slug", "label", "primary", "mu_type", "short_name")
        )

        context["management_units"] = mus

        return context


class Grid5List(ListView):

    template_name = "common/grid5_list.html"
    model = Grid5
    queryset = Grid5.objects.prefetch_related("lake").all()


class Grid5Detail(DetailView):

    template_name = "common/grid5_detail.html"
    model = Grid5
    queryset = Grid5.objects.all()

    def get_context_data(self, **kwargs):
        """Add the list management units associated with this grid.
        We add them to the context so that they come back in one query and
        can have the lake associated them before hand.

        """

        context = super().get_context_data(**kwargs)
        context["mus"] = ManagementUnit.objects.filter(
            grids__slug=self.kwargs["slug"]
        ).prefetch_related("lake", "lake_management_unit_type")

        return context


class ManagementUnitList(ListView):

    template_name = "common/management_unit_list.html"
    model = ManagementUnit

    def get_queryset(self):
        qs = ManagementUnit.objects.prefetch_related(
            "lake",
            "lake_management_unit_type",
            "lake_management_unit_type__management_unit_type",
        ).all()
        return qs


class ManagementUnitDetail(DetailView):

    template_name = "common/management_unit_detail.html"
    model = ManagementUnit
    queryset = ManagementUnit.objects.all()

    def get_context_data(self, **kwargs):
        """Add the list of grids associated with this management unit.
        Add them to the context so tha they come back in one query and
        can be grouped with our helper function.

        """
        ncol = 6
        context = super().get_context_data(**kwargs)
        grids = (
            Grid5.objects.filter(managementunit__slug=self.kwargs["slug"])
            .prefetch_related("lake")
            .order_by("grid")
        )
        context["grids"] = grouped(grids, ncol)

        return context
