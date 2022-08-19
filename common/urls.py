from django.urls import path, include
from .views import SpeciesList, Grid5List, LakeList, ManagementUnitList

from .api import urls as api_urls

app_name = "common"

urlpatterns = [
    path("lakes", LakeList.as_view(), name="lake_list"),
    path("species", SpeciesList.as_view(), name="species_list"),
    path("grid5s", Grid5List.as_view(), name="grid5_list"),
    path("management_units", ManagementUnitList.as_view(), name="management_unit_list"),
    path("api/v1/", include(api_urls, namespace="common_api")),    
]
