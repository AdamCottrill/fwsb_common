"""Views for the api for our common models

The veiws in this file should all be publicly available as readonly.

"""

from django.db.models import F, Case, Value, When
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import (
    Grid5,
    Lake,
    LakeManagementUnitType,
    ManagementUnit,
    ManagementUnitType,
    Species,
    Taxon,
    BottomType,
    CoverType,
    Vessel
)
from .filters import (
    Grid5Filter,
    LakeFilter,
    ManagementUnitFilter,
    SpeciesFilter,
    TaxonFilter,
    LakeManagementUnitTypeFilter,
)
from .serializers import (
    Flen2TlenSerializer,
    Grid5DetailSerializer,
    Grid5Serializer,
    LakeDetailSerializer,
    LakeManagementUnitTypeSerializer,
    LakeSerializer,
    ManagementUnitSerializer,
    ManagementUnitTypeSerializer,
    SpeciesDetailSerializer,
    SpeciesSerializer,
    TaxonSerializer,
    LookupTableSerializer,
)
from .utils import parse_point


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class LakeListView(generics.ListAPIView):

    pagination_class = None
    queryset = Lake.objects.all()
    serializer_class = LakeSerializer
    filterset_class = LakeFilter


class LakeDetailView(generics.RetrieveAPIView):

    queryset = Lake.objects.all()
    serializer_class = LakeDetailSerializer
    lookup_field = "abbrev"


class ManagementUnitTypeListView(generics.ListAPIView):

    queryset = ManagementUnitType.objects.all()
    serializer_class = ManagementUnitTypeSerializer
    pagination_class = None


class LakeManagementUnitTypeListView(generics.ListAPIView):

    serializer_class = LakeManagementUnitTypeSerializer
    filterset_class = LakeManagementUnitTypeFilter
    pagination_class = None

    def get_queryset(self):
        qs = (
            LakeManagementUnitType.objects.all()
            .prefetch_related("lake", "management_unit_type")
            .annotate(
                lake_name=F("lake__lake_name"),
                lake_abbrev=F("lake__abbrev"),
                mu_type_label=F("management_unit_type__label"),
                mu_type_abbrev=F("management_unit_type__abbrev"),
            )
            .values(
                "lake_name",
                "lake_abbrev",
                "mu_type_label",
                "mu_type_abbrev",
                "primary",
                "id",
            )
        )
        return qs


class ManagementUnitListView(generics.ListAPIView):

    pagination_class = StandardResultsSetPagination
    serializer_class = ManagementUnitSerializer
    filterset_class = ManagementUnitFilter

    def get_queryset(self):
        qs = (
            ManagementUnit.objects.order_by("slug")
            .select_related("lake_management_unit_type__management_unit_type")
            .annotate(
                mu_type=F("lake_management_unit_type__management_unit_type__label"),
                mu_type_slug=F("lake_management_unit_type__management_unit_type__slug"),
                lake_abbrev=F("lake__abbrev"),
            )
            .values(
                "id",
                "lake_abbrev",
                "mu_type",
                "mu_type_slug",
                "slug",
                "label",
                "centroid",
                "envelope",
            )
        )

        return qs


class ManagementUnitDetailView(generics.RetrieveAPIView):

    serializer_class = ManagementUnitSerializer
    lookup_field = "slug"

    def get_queryset(self):
        qs = (
            ManagementUnit.objects.order_by("slug")
            .select_related("lake_management_unit_type__management_unit_type")
            .annotate(
                mu_type=F("lake_management_unit_type__management_unit_type__label"),
                mu_type_slug=F("lake_management_unit_type__management_unit_type__slug"),
                lake_abbrev=F("lake__abbrev"),
            )
            .values(
                "id",
                "lake_abbrev",
                "mu_type",
                "mu_type_slug",
                "slug",
                "label",
                "centroid",
                "envelope",
            )
        )

        return qs


class Grid5ListView(generics.ListAPIView):

    pagination_class = StandardResultsSetPagination
    # queryset = Grid5.objects.all().prefetch_related("lake")
    serializer_class = Grid5Serializer
    filterset_class = Grid5Filter

    def get_queryset(self):
        qs = Grid5.objects.annotate(lake_abbrev=F("lake__abbrev"),).values(
            "id",
            "lake_abbrev",
            "grid",
            "slug",
            "centroid",
        )
        return qs


class Grid5DetailView(generics.RetrieveAPIView):

    queryset = Grid5.objects.all()
    serializer_class = Grid5DetailSerializer
    lookup_field = "slug"


class SpeciesListView(generics.ListAPIView):

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    filterset_class = SpeciesFilter
    pagination_class = None


class SpeciesDetailView(generics.RetrieveAPIView):

    queryset = Species.objects.all()
    serializer_class = SpeciesDetailSerializer
    lookup_field = "spc"


class TaxonListView(generics.ListAPIView):

    serializer_class = TaxonSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = TaxonFilter

    def get_queryset(self):

        qs = Taxon.objects.all().values(
            "taxon",
            "itiscode",
            "taxon_name",
            "taxon_label",
            "taxonomic_rank",
            "vertinvert",
            "omnr_provincial_code",
        )
        return qs


class BottomTypeListView(generics.ListAPIView):

    serializer_class = LookupTableSerializer
    pagination_class = None

    def get_queryset(self):

        all = self.request.query_params.get("all", "")
        if all.lower() in ["true", "1", "t"]:
            qs = BottomType.all_objects.all()
        else:
            qs = BottomType.objects.all()

        qs = qs.annotate(
            is_active=Case(
                When(obsolete_date__isnull=True, then=True),
                When(obsolete_date__isnull=False, then=False),
                default=Value(None),
            )
        ).values(
            "id",
            "abbrev",
            "label",
            "description",
            "slug",
            "is_active",
        )

        return qs


class CoverTypeListView(generics.ListAPIView):

    serializer_class = LookupTableSerializer
    pagination_class = None

    def get_queryset(self):

        all = self.request.query_params.get("all", "")
        if all.lower() in ["true", "1", "t"]:
            qs = BottomType.all_objects.all()
        if all:
            qs = CoverType.all_objects.all()
        else:
            qs = CoverType.objects.all()

        qs = qs.annotate(
            is_active=Case(
                When(obsolete_date__isnull=True, then=True),
                When(obsolete_date__isnull=False, then=False),
                default=Value(None),
            )
        ).values(
            "id",
            "abbrev",
            "label",
            "description",
            "slug",
            "is_active",
        )

        return qs


class VesselListView(generics.ListAPIView):

    serializer_class = LookupTableSerializer
    pagination_class = None

    def get_queryset(self):

        all = self.request.query_params.get("all", "")
        if all.lower() in ["true", "1", "t"]:
            qs = Vessel.all_objects.all()
        else:
            qs = Vessel.objects.all()

        qs = qs.annotate(
            is_active=Case(
                When(obsolete_date__isnull=True, then=True),
                When(obsolete_date__isnull=False, then=False),
                default=Value(None),
            )
        ).values(
            "id",
            "abbrev",
            "label",
            "description",
            "slug",
            "is_active",
        )

        return qs



class Flen2TlenListView(generics.ListAPIView):
    """An api endpoint that returns the flen-tlen regression coefficents
    for our species. Uses a species filter to select subsets based on
    species name or species code.

    """

    queryset = (
        Species.objects.filter(flen2tlen_alpha__isnull=False)
        .all()
        .values("spc", "flen2tlen_alpha", "flen2tlen_beta")
    )
    serializer_class = Flen2TlenSerializer
    filterset_class = SpeciesFilter
    pagination_class = None


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
        lake_abbrev=obj.lake.abbrev,
        label=obj.label,
        mu_type=obj.lake_management_unit_type.management_unit_type.label,
        mu_type_slug=obj.lake_management_unit_type.management_unit_type.slug,
        slug=obj.slug,
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

    qs = ManagementUnit.objects.select_related(
        "lake_management_unit_type", "lake_management_unit_type__management_unit_type"
    ).filter(geom__contains=pt)

    if all_mus and all_mus in ["T", "t", "TRUE", "True", "true"]:
        qs = qs.all()
    elif mu_type:
        qs = qs.filter(
            lake_management_unit_type__management_unit_type__slug=mu_type
        ).first()
    else:
        qs = qs.filter(lake_management_unit_type__primary=True).first()

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
        .filter(lake_management_unit_type__management_unit_type__slug="stat_dist")
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
