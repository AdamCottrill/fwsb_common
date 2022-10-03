from django.contrib import admin

from ..models import Species


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    search_fields = ["spc_nmco", "spc_nmsc", "spc"]
    list_display = ("spc", "spc_nmco", "spc_nmsc", "abbrev")
