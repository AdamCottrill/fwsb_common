from django.contrib import admin

from .models import Lake, ManagementUnit, Species, Grid5

admin.site.empty_value_display = '(None)'


@admin.register(Lake)
class LakeModelAdmin(admin.ModelAdmin):
    list_display = ('lake_name', 'abbrev')


@admin.register(ManagementUnit)
class ManagementUnitModelAdmin(admin.ModelAdmin):
    list_display = ('label', 'lake', 'mu_type', 'description')
    list_filter = ('lake', 'mu_type')


@admin.register(Species)
class SpeciesModelAdmin(admin.ModelAdmin):
    list_display = ('spc', 'spc_nmco', 'spc_nmsc', 'abbrev')


@admin.register(Grid5)
class Grid5ModelAdmin(admin.ModelAdmin):
    list_display = ('grid', 'slug', 'lake')
