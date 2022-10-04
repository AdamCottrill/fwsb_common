from django.urls import path, re_path, include
from .views import (
    SpeciesList,
    SpeciesDetail,
    TaxonList,
    Grid5List,
    Grid5Detail,
    LakeList,
    LakeDetail,
    ManagementUnitList,
    ManagementUnitDetail,
)

from .api import urls as api_urls

app_name = "common"

urlpatterns = [
    path("lakes", LakeList.as_view(), name="lake_list"),
    re_path(r"lake/(?P<abbrev>[A-Z]{2})/", LakeDetail.as_view(), name="lake_detail"),
    path("species", SpeciesList.as_view(), name="species_list"),
    re_path(
        r"species/(?P<spc>[0-9]{3})/", SpeciesDetail.as_view(), name="species_detail"
    ),
    path("taxon", TaxonList.as_view(), name="taxon_list"),
    path("grid5s", Grid5List.as_view(), name="grid5_list"),
    path("grid5/<slug:slug>/", Grid5Detail.as_view(), name="grid5_detail"),
    path("management_units", ManagementUnitList.as_view(), name="management_unit_list"),
    path(
        "management_unit/<slug:slug>/",
        ManagementUnitDetail.as_view(),
        name="management_unit_detail",
    ),
    path("api/v1/", include(api_urls, namespace="common_api")),
]
