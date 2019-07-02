"""urls for the api for our common models"""

from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (SpeciesViewSet, LakeViewSet, ManagementUnitViewSet,
                    Grid5ViewSet)

app_name = "common"

router = SimpleRouter()

router.register('lake', LakeViewSet)
router.register('management_unit', ManagementUnitViewSet)
router.register('grid5', Grid5ViewSet)
router.register('species', SpeciesViewSet)

urlpatterns = router.urls

urlpatterns += []
