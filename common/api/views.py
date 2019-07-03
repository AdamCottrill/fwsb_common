"""Views for the api for our common models

The veiws in this file should all be publicly available as readonly.

"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Species, Lake, ManagementUnit, Grid5

from .serializers import (
    SpeciesSerializer,
    LakeSerializer,
    ManagementUnitSerializer,
    Grid5Serializer,
)


class LakeViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Lake.objects.all()
    serializer_class = LakeSerializer


class ManagementUnitViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ManagementUnit.objects.all()
    serializer_class = ManagementUnitSerializer
    # filterset_class = ManagementUnitFilter
    lookup_field = "slug"


class SpeciesViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    lookup_field = "spc"


class Grid5ViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Grid5.objects.all()
    serializer_class = Grid5Serializer
