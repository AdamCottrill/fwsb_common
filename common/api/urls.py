"""urls for the api for our common models"""

from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    SpeciesListView,  # LakeViewSet,
    SpeciesDetailView,
    TaxonListView,
    Flen2TlenListView,
    LakeDetailView,
    LakeListView,
    ManagementUnitTypeListView,
    LakeManagementUnitTypeListView,
    ManagementUnitListView,
    ManagementUnitDetailView,
    Grid5ListView,
    Grid5DetailView,
    BottomTypeListView,
    CoverTypeListView,
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
    path("lakes/", LakeListView.as_view(), name="lake-list"),
    path("lake/<str:abbrev>", LakeDetailView.as_view(), name="lake-detail"),
    path(
        "management_unit_types/",
        ManagementUnitTypeListView.as_view(),
        name="management_unit_type-list",
    ),
    path(
        "lake_management_unit_types/",
        LakeManagementUnitTypeListView.as_view(),
        name="lake_management_unit_type-list",
    ),
    path(
        "management_units/",
        ManagementUnitListView.as_view(),
        name="management_unit-list",
    ),
    path(
        "management_unit/<slug:slug>",
        ManagementUnitDetailView.as_view(),
        name="management_unit-detail",
    ),
    path("grid5s/", Grid5ListView.as_view(), name="grid5-list"),
    path("grid5/<slug:slug>", Grid5DetailView.as_view(), name="grid5-detail"),
    path("species/", SpeciesListView.as_view(), name="species-list"),
    path("taxon/", TaxonListView.as_view(), name="taxon-list"),
    path("species/<str:spc>", SpeciesDetailView.as_view(), name="species-detail"),
    path("bottom_types/", BottomTypeListView.as_view(), name="bottom-type-list"),
    path("cover_types/", CoverTypeListView.as_view(), name="cover-type-list"),
    path("flen2tlen/", Flen2TlenListView.as_view(), name="flen2tlen-list"),
    path("spatial_lookup/lake/", get_lake_from_pt, name="api-lookup-lake-from-pt"),
    path(
        "spatial_lookup/management_unit/",
        get_management_unit_from_pt,
        name="api-lookup-management-unit-from-pt",
    ),
    path("spatial_lookup/grid5/", get_grid5_from_pt, name="api-lookup-grid5-from-pt"),
    path("spatial_lookup/", pt_spatial_attrs, name="api-lookup-spatial-attrs"),
]
