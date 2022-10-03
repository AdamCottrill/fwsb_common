from django import forms
from django.contrib import admin
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


class CsvImportForm(forms.Form):
    csv_file = forms.FileField(
        widget=forms.FileInput(attrs={"accept": ".csv"}),
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
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
