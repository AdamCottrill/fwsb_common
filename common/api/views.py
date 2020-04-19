"""Views for the api for our common models

The veiws in this file should all be publicly available as readonly.

"""

from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from ..models import Species, Lake, ManagementUnit, Grid5

from .filters import Grid5Filter, ManagementUnitFilter
from .utils import parse_point

from .serializers import (
    SpeciesSerializer,
    SpeciesDetailSerializer,
    LakeSerializer,
    LakeDetailSerializer,
    ManagementUnitSerializer,
    ManagementUnitDetailSerializer,
    Grid5Serializer,
    Grid5DetailSerializer,
)


class LakeListView(generics.ListAPIView):

    queryset = Lake.objects.all()
    serializer_class = LakeSerializer


class LakeDetailView(generics.RetrieveAPIView):

    queryset = Lake.objects.all()
    serializer_class = LakeDetailSerializer
    lookup_field = "abbrev"


class ManagementUnitListView(generics.ListAPIView):

    queryset = ManagementUnit.objects.all().prefetch_related("lake")
    serializer_class = ManagementUnitSerializer
    filterset_class = ManagementUnitFilter


class ManagementUnitDetailView(generics.RetrieveAPIView):

    queryset = ManagementUnit.objects.all()
    serializer_class = ManagementUnitDetailSerializer
    lookup_field = "slug"


class Grid5ListView(generics.ListAPIView):

    queryset = Grid5.objects.all().prefetch_related("lake")
    serializer_class = Grid5Serializer
    filterset_class = Grid5Filter


class Grid5DetailView(generics.RetrieveAPIView):

    queryset = Grid5.objects.all()
    serializer_class = Grid5DetailSerializer
    lookup_field = "slug"


class SpeciesListView(generics.ListAPIView):

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class SpeciesDetailView(generics.RetrieveAPIView):

    queryset = Species.objects.all()
    serializer_class = SpeciesDetailSerializer
    lookup_field = "spc"


@api_view(["POST"])
@permission_classes([AllowAny])
def get_lake_from_pt(request):
    """This function accepts post requests that contain a geojson
    representation of a point.  The view returns a dictionary contianing
    the id, abbreviation, name, centroid and bounds (extent) of the lake
    containing the point, or an empty dictionary if the dat is not geojson
    or falls outside of any lake.

    TODO: add options for 'pure' and 'plus' geometries

    """

    geom = request.query_params.get("geom")
    pt = parse_point(request.data.get("point"))
    if pt is None:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    lake = Lake.objects.filter(geom__contains=pt).first()

    if lake:
        ret = dict(
            id=lake.id,
            abbrev=lake.abbrev,
            lake_name=lake.lake_name,
            centroid=lake.centroid.wkt if lake.centroid else "",
            envelope=lake.envelope.wkt if lake.envelope else "",
            centroid_ontario=lake.centroid_ontario.wkt if lake.centroid_ontario else "",
            envelope_ontario=lake.envelope_ontario.wkt if lake.envelope_ontario else "",
        )

        # return one geom or the other - not both
        if geom == "geom":
            ret["geom"] = lake.geom.geojson
        elif geom == "geom_ontario":
            ret["geom"] = lake.geom_ontario.geojson

        return Response(ret, status=status.HTTP_200_OK)
    else:
        # no lake object could be associated with that point.
        # 400
        return Response({}, status=status.HTTP_404_NOT_FOUND)


def manUnit_dict(obj, geom=None):
    """Serialize a management unit to a python dictionary

    Arguments:
    - `obj`: a ManagementUnit instance
    """

    item = dict(
        id=obj.id,
        slug=obj.slug,
        label=obj.label,
        mu_type=obj.mu_type,
        centroid=obj.centroid.wkt,
        envelope=obj.envelope.wkt,
    )

    if geom == "geom":
        item["geom"] = obj.geom.geojson

    return item


@api_view(["POST"])
@permission_classes([AllowAny])
def get_management_unit_from_pt(request):
    """This function accepts post requests that contains a geojson
    representation of a point.  The view returns a dictionary contianing
    the id, label, mu_type, centroid and bounds (extent) of the management_unit
    containing the point, or an empty dictionary if the data is not geojson
    or falls outside of any management_unit.

    This function takes an additional argument (mu_type) as a query
    parameter that controls what type of managemnet unit is returned -
    current options are stat_dist, mu, qma, ltrz.  Others could be
    added in the future.  If the mu_type argument is not included in
    the request, the management_unit with primary=True is returned by
    default.

    TODO: add options for 'pure' and 'plus' geometries

    """
    geom = request.query_params.get("geom")
    mu_type = request.query_params.get("mu_type")
    all_mus = request.query_params.get("all")

    pt = parse_point(request.data.get("point"))
    if pt is None:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    qs = ManagementUnit.objects.filter(geom__contains=pt)

    if all_mus and all_mus in ["T", "t", "TRUE", "True", "true"]:
        qs = qs.all()
    elif mu_type:
        qs = qs.filter(mu_type=mu_type).first()
    else:
        qs = qs.filter(primary=True).first()

    if qs:
        if all_mus:
            ret = [manUnit_dict(x, geom) for x in qs]
        else:
            ret = manUnit_dict(qs, geom)

        return Response(ret, status=status.HTTP_200_OK)
    else:
        # no qs object could be associated with that point.
        # 400
        return Response({}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_grid5_from_pt(request):
    """This function accepts post requests that contain a geojson
    representation of a point.  The view returns a dictionary contianing
    the id, abbreviation, name, centroid and bounds (extent) of the grid5
    containing the point, or an empty dictionary if the dat is not geojson
    or falls outside of any grid5.

    TODO: Add polygon field for grid5 objects so that we can find out
    which grid the point falls in. This function finds the closest
    centroid which is slower and likely to have lots of failing edge
    cases.

    post request should be of the form:

    {"point": "POINT(-81.5 44.5)"}

    """

    pt = parse_point(request.data.get("point"))
    if pt is None:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    grid5 = Grid5.objects.select_related("lake").filter(geom__contains=pt).first()

    geom = request.query_params.get("geom")

    if grid5:
        ret = dict(
            id=grid5.id,
            grid=grid5.grid,
            slug=grid5.slug,
            centroid=grid5.centroid.wkt,
            envelope=grid5.envelope.wkt,
            # lake attributes:
            lake=dict(
                lake_id=grid5.lake.id,
                lake_abbrev=grid5.lake.abbrev,
                lake_name=grid5.lake.lake_name,
            ),
        )
        if geom == "geom":
            ret["geom"] = grid5.geom.geojson

        return Response(ret, status=status.HTTP_200_OK)
    else:
        # no grid5 object could be associated with that point.
        # 400
        return Response({}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([AllowAny])
def pt_spatial_attrs(request):
    """This function accepts post requests that contain a geojson
    representation of a point and returns a dictionary containing the
    basic lake, management unit(s) and 5-minute grid that contains that point.  Given a lat-lon, return
    a dictionary with the following elements:

    + lake - with id, lake name, lake abbrev
    + manUnit(s) - [(id, label), ....]
    + grid5 - id, label, lake abbrev.

    post data should contain a json string of the form:

    {"point": "POINT(-81.5 44.5)"}

    TODO: implement the mangement unit array.

    """

    pt = parse_point(request.data.get("point"))
    if pt is None:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    ret = dict()

    lake = Lake.objects.filter(geom__contains=pt).first()
    if lake:
        ret["lake"] = dict(
            id=lake.id,
            abbrev=lake.abbrev,
            lake_name=lake.lake_name,
            centroid=lake.centroid.wkt,
        )
    else:
        ret["lake"] = ""

    manUnit = (
        ManagementUnit.objects.filter(geom__contains=pt)
        .filter(mu_type="stat_dist")
        .first()
    )
    if manUnit:
        ret["manUnit"] = dict(
            id=manUnit.id,
            slug=manUnit.slug,
            label=manUnit.label,
            centroid=manUnit.centroid.wkt,
        )
    else:
        ret["manUnit"] = ""

    grid5 = Grid5.objects.select_related("lake").filter(geom__contains=pt).first()

    if grid5:
        ret["grid5"] = dict(
            id=grid5.id,
            grid=grid5.grid,
            slug=grid5.slug,
            centroid=grid5.centroid.wkt,
            lake_abbrev=grid5.lake.abbrev,
        )
    else:
        ret["grid5"] = ""

    return Response(ret, status=status.HTTP_200_OK)
