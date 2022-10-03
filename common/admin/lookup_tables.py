from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from ..models import (
    CoverType,
    BottomType,
)


class ObsoleteLookupFilter(admin.SimpleListFilter):

    title = _("Active Status")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "is_obsolete"

    def lookups(self, request, model_geoadmin):
        """ """
        return (
            ("obsolete", _("Obsolete")),
            ("active", _("Active")),
        )

    def queryset(self, request, queryset):
        if self.value() == "obsolete":
            return queryset.filter(obsolete_date__isnull=False)
        if self.value() == "active":
            return queryset.exclude(obsolete_date__isnull=False)
        return queryset


@admin.register(BottomType)
class BottomTypeAdmin(admin.ModelAdmin):
    search_fields = ["abbrev", "label"]
    list_display = ("abbrev", "label", "is_active")
    list_filter = [
        ObsoleteLookupFilter,
    ]

    def is_active(self, obj):
        return obj.obsolete_date is None


@admin.register(CoverType)
class CoverTypeAdmin(admin.ModelAdmin):
    search_fields = ["abbrev", "label"]
    list_display = ("abbrev", "label", "is_active")
    list_filter = [
        ObsoleteLookupFilter,
    ]

    def is_active(self, obj):
        return obj.obsolete_date is None
