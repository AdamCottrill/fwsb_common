"""Serializers for our common models.

Serializers convert our data base objects to json and back again (if
needed).

  """

from rest_framework import serializers
from ..models import Species, Lake, ManagementUnit, Grid5


class LakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lake
        fields = ('abbrev', 'lake_name')
        lookup_field = 'abbrev'


class ManagementUnitSerializer(serializers.ModelSerializer):

    lake = LakeSerializer()

    class Meta:
        model = ManagementUnit
        fields = ('label', 'lake', 'mu_type')


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ('spc', 'abbrev', 'spc_nmco', 'spc_nmsc', 'spc_nmfam')
        lookup_field = 'spc'

class Grid5Serializer(serializers.ModelSerializer):

    lake = LakeSerializer()

    class Meta:
        model = Grid5
        fields = ('grid', 'lake', 'slug')
        lookup_field = 'slug'
