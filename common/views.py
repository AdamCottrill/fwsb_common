from django.shortcuts import render, get_object_or_404

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Grid5, Lake, ManagementUnit, Species


def grouped(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


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
        context["management_units"] = ManagementUnit.objects.filter(
            lake__abbrev=self.kwargs["abbrev"]
        ).values("slug", "label", "primary", "mu_type")
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
        ).prefetch_related("lake")

        return context


class ManagementUnitList(ListView):

    template_name = "common/management_unit_list.html"
    model = ManagementUnit
    queryset = ManagementUnit.objects.prefetch_related("lake").all()


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
