"""Serializers for our common models.

Serializers convert our data base objects to json and back again (if
needed).

  """


from rest_framework import serializers
from ..models import Species, Lake, ManagementUnit, Grid5


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class LakeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Lake
        fields = ("abbrev", "lake_name")
        lookup_field = "abbrev"


class LakeDetailSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Lake
        fields = (
            "abbrev",
            "lake_name",
            "centroid",
            "envelope",
            "centroid_ontario",
            "envelope_ontario",
        )
        lookup_field = "abbrev"


class LakeManagementUnitTypeSerializer(serializers.Serializer):
    """"""

    id = serializers.IntegerField(read_only=True)
    lake_abbrev = serializers.CharField(read_only=True)
    lake_name = serializers.CharField(read_only=True)
    mu_type_abbrev = serializers.CharField(read_only=True)
    mu_type_label = serializers.CharField(read_only=True)
    primary = serializers.BooleanField(read_only=True)


class ManagementUnitTypeSerializer(serializers.Serializer):
    """"""

    id = serializers.IntegerField(read_only=True)
    abbrev = serializers.CharField(read_only=True)
    label = serializers.CharField(read_only=True)
    desciption = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)


class ManagementUnitSerializer(serializers.Serializer):
    """"""

    id = serializers.IntegerField(read_only=True)
    lake_abbrev = serializers.CharField(read_only=True)
    label = serializers.CharField(read_only=True)
    mu_type = serializers.CharField(read_only=True)
    mu_type_slug = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    centroid = serializers.CharField(read_only=True)
    envelope = serializers.CharField(read_only=True)


class Grid5Serializer(serializers.Serializer):
    """"""

    id = serializers.IntegerField(read_only=True)
    lake_abbrev = serializers.CharField(read_only=True)
    grid = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    centroid = serializers.CharField(read_only=True)


# class Grid5Serializer(serializers.ModelSerializer):
#
#    lake = LakeSerializer(fields=["abbrev", "lake_name"])
#
#    class Meta:
#        model = Grid5
#        fields = ("grid", "lake", "slug", "centroid")
#        lookup_field = "slug"
#


class Grid5DetailSerializer(serializers.ModelSerializer):

    lake = LakeSerializer(fields=["abbrev", "lake_name"])

    class Meta:
        model = Grid5
        fields = ("grid", "lake", "slug", "centroid", "envelope")
        lookup_field = "slug"


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ("spc", "spc_nmco", "spc_nmsc")
        lookup_field = "spc"


class Flen2TlenSerializer(serializers.ModelSerializer):

    intercept = serializers.FloatField(read_only=True, source="flen2tlen_alpha")
    slope = serializers.FloatField(read_only=True, source="flen2tlen_beta")

    class Meta:
        model = Species
        fields = ("spc", "intercept", "slope")
        lookup_field = "spc"


class SpeciesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ("spc", "abbrev", "spc_nmco", "spc_nmsc", "spc_nmfam", "spc_lab")
        lookup_field = "spc"


class LookupTableSerializer(serializers.Serializer):
    """"""

    id = serializers.IntegerField(read_only=True)
    abbrev = serializers.CharField(read_only=True)
    label = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
