"""urls for the api for our common models"""

from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    SpeciesListView,  # LakeViewSet,
    SpeciesDetailView,
    LakeDetailView,
    LakeListView,
    ManagementUnitListView,
    ManagementUnitDetailView,
    Grid5ListView,
    Grid5DetailView,
    #    spatial_lookup,
    get_lake_from_pt,
    get_management_unit_from_pt,
    get_grid5_from_pt,
    pt_spatial_attrs,
)

app_name = "common"

router = SimpleRouter()

# router.register('lake', LakeViewSet)
# router.register("management_unit", ManagementUnitViewSet)
# router.register("grid5", Grid5ViewSet)
# router.register("species", SpeciesViewSet)

urlpatterns = router.urls

urlpatterns += [
    path("lakes/", LakeListView.as_view()),
    path("lake/<str:abbrev>", LakeDetailView.as_view()),
    path("management_units/", ManagementUnitListView.as_view()),
    path("management_unit/<slug:slug>", ManagementUnitDetailView.as_view()),
    path("grid5s/", Grid5ListView.as_view()),
    path("grid5/<slug:slug>", Grid5DetailView.as_view()),
    path("species/", SpeciesListView.as_view()),
    path("species/<str:spc>", SpeciesDetailView.as_view()),
    path("spatial_lookup/lake/", get_lake_from_pt, name="api-lookup-lake-from-pt"),
    path(
        "spatial_lookup/management_unit/",
        get_management_unit_from_pt,
        name="api-lookup-management-unit-from-pt",
    ),
    path("spatial_lookup/grid5/", get_grid5_from_pt, name="api-lookup-grid5-from-pt"),
    path("spatial_lookup/", pt_spatial_attrs, name="api-lookup-spatial-attrs"),
]
