from django.contrib.gis import admin
from django import forms
from .models import Lake, ManagementUnit, Species, Grid5, ManagementUnitType,  LakeManagementUnitType

admin.site.empty_value_display = "(None)"


class ManagementUnitChangeForm(forms.ModelForm):
    class Meta:
        model = ManagementUnit
        fields = [
            "lake",
            "label",
            "description",
            "geom",
            "centroid",
            "envelope",
            # "primary",
            # "mu_type",
            "grids",
        ]

    def __init__(self, *args, **kwargs):
        super(ManagementUnitChangeForm, self).__init__(*args, **kwargs)
        my_model = self.instance
        self.fields["grids"].queryset = (
            Grid5.objects.filter(lake_id=my_model.lake.id)
            .select_related("lake")
            .defer(
                "geom",
                "envelope",
                "centroid",
                "lake__geom",
                "lake__envelope",
                "lake__centroid",
                "lake__geom_ontario",
                "lake__envelope_ontario",
                "lake__centroid_ontario",
            )
        )


class ManagementUnitCreationForm(forms.ModelForm):
    class Meta:
        model = ManagementUnit
        fields = [
            "lake",
            "label",
            "description",
            "geom",
            "centroid",
            "envelope",
            # "primary",
            # "mu_type",
            "grids",
        ]

    def save(self, commit=True):
        my_model = super(ManagementUnitCreationForm, self).save(commit=False)
        my_model.save()
        return my_model


@admin.register(ManagementUnit)
class ManagementUnitAdmin(admin.ModelAdmin):
    # list_display = ("label", "lake", "mu_type", "description")
    # list_filter = ("lake", "mu_type")

    list_display = ("label", "lake", "description")
    list_filter = ("lake",)
    list_select_related = ("lake",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("lake").defer(
            "lake__geom", "lake__envelope", "lake__centroid"
        )
        return queryset

    form = ManagementUnitChangeForm
    add_form = ManagementUnitCreationForm

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(ManagementUnitAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during ManagementUnit creation
        """
        defaults = {}
        if obj is None:
            defaults.update(
                {
                    "form": self.add_form,
                    "fields": admin.util.flatten_fieldsets(self.add_fieldsets),
                }
            )
        defaults.update(kwargs)
        return super(ManagementUnitAdmin, self).get_form(request, obj, **defaults)



@admin.register(ManagementUnitType)
class ManagementUnitType(admin.OSMGeoAdmin):
    list_display = ("abbrev", "label")
    readonly_fields = ["slug",]

    
@admin.register(LakeManagementUnitType)
class LakeManagementUnitType(admin.OSMGeoAdmin):
    list_display = ("lake", "management_unit_type", "primary")
    list_filter = ( "primary", "lake", "management_unit_type")

    def lake(obj):
        return f"{obj.lake.lake_name} ({obj.lake.abbrev})"
    def management_unit_type(obj):
        return f"{obj.management_unit_type.label} ({obj.management_unit_type.abbrev})"

@admin.register(Lake)
class LakeAdmin(admin.OSMGeoAdmin):
    list_display = ("lake_name", "abbrev")

    
@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    search_fields = ["spc_nmco", "spc_nmsc", "spc"]
    list_display = ("spc", "spc_nmco", "spc_nmsc", "abbrev")


@admin.register(Grid5)
class Grid5Admin(admin.ModelAdmin):
    search_fields = ["grid"]
    list_display = ("grid", "slug", "lake")
    list_filter = ("lake",)
    list_select_related = ("lake",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("lake").defer(
            "geom",
            "envelope",
            "centroid",
            "lake__geom",
            "lake__envelope",
            "lake__centroid",
            "lake__geom_ontario",
            "lake__envelope_ontario",
            "lake__centroid_ontario",
        )
        return queryset
