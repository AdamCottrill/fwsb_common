from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Grid5, Lake, ManagementUnit, Species


class SpeciesList(ListView):

    template_name = "common/species_list.html"
    model = Species
    queryset = Species.objects.all()

    
class LakeList(ListView):

    template_name = "common/lake_list.html"
    model = Lake
    queryset = Lake.objects.all()

class Grid5List(ListView):

    template_name = "common/grid5_list.html"
    model = Grid5
    queryset = Grid5.objects.prefetch_related('lake').all()

    
class ManagementUnitList(ListView):

    template_name = "common/management_unit_list.html"
    model = ManagementUnit
    queryset = ManagementUnit.objects.prefetch_related('lake').all()

    
    


# SpeciesList
# SpeciesDetail
# LakeList
# Grid5List
# Grid5List
# ManagementUnitList
# ManagementUnitDetail
