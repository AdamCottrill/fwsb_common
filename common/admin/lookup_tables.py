import csv

from django.contrib import admin, messages
from django.db import transaction
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.utils.translation import gettext_lazy as _
from django.urls import path

from ..models import BottomType, CoverType, Vessel
from .admin_utils import ObsoleteLookupFilter, CsvImportForm


class LookupAdminBase(admin.ModelAdmin):
    """This is a base model that includes csv lookup
    functionality. The csv lookup assumes that the associated file
    (and model) have attributes 'abbrev' and 'label'. There is minimal
    validation, error-trapping or testing of this functionality as it
    intended to used infrequently by administrative users only.

    """

    change_list_template = "common/lookup_table_changelist.html"

    def is_active(self, obj):
        return obj.obsolete_date is None

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith(".csv"):
                messages.error(request, "The wrong file type was uploaded.")
                return HttpResponseRedirect(request.path_info)

            decoded_file = csv_file.read().decode("utf-8-sig").splitlines()
            data = csv.DictReader(decoded_file)
            try:
                with transaction.atomic():
                    for item in list(data):
                        obj, created = self.model.objects.get_or_create(
                            abbrev=item.get("abbrev"), label=item.get("label")
                        )
                        obj.save()
                    msg = f"Your {self.model.__name__} file has been successfully imported."
                    messages.success(request, msg)
            except:
                msg = (
                    "Something went wrong! "
                    "Please double check your file and its contents and try again."
                )
                messages.error(request, msg)
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form, "model_name": self.model.__name__}
        return render(request, "admin/csv_form.html", payload)


@admin.register(BottomType)
class BottomTypeAdmin(LookupAdminBase):
    search_fields = ["abbrev", "label"]
    list_display = ("abbrev", "label", "is_active")
    list_filter = [
        ObsoleteLookupFilter,
    ]


@admin.register(CoverType)
class CoverTypeAdmin(LookupAdminBase):
    search_fields = ["abbrev", "label"]
    list_display = ("abbrev", "label", "is_active")
    list_filter = [
        ObsoleteLookupFilter,
    ]


@admin.register(Vessel)
class VesselAdmin(LookupAdminBase):
    search_fields = ["abbrev", "label"]
    list_display = ("abbrev", "label", "is_active")
    list_filter = [
        ObsoleteLookupFilter,
    ]
