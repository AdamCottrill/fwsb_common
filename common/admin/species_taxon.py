import csv

from django.contrib import admin, messages
from django.db import transaction
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import path
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from ..models import Species, Taxon
from .admin_utils import CsvImportForm


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    search_fields = ["spc_nmco", "spc_nmsc", "spc"]
    list_display = ("spc", "spc_nmco", "spc_nmsc", "abbrev")


def add_csv_taxon(csv_data):
    with transaction.atomic():
        for item in csv_data:
            # this says in python:
            parent_tsn = item.pop("parent_tsn")
            itiscode = item.get("itiscode")
            taxon = Taxon.objects.filter(itiscode=itiscode).first()
            if taxon:
                continue
            parent = Taxon.objects.filter(itiscode=parent_tsn).first()
            if parent_tsn == 0 or parent is None:
                parent = Taxon.add_root(**item)
            else:
                parent.add_child(**item)


class TaxonAdmin(TreeAdmin):

    list_display = [
        "__str__",
        "taxon_name",
        "taxon_label",
        "taxonomic_rank",
        "vertinvert",
    ]
    list_filter = ["taxonomic_rank", "vertinvert"]
    search_fields = ["taxon", "itiscode", "taxon_name", "taxon_label"]

    form = movenodeform_factory(Taxon)

    change_list_template = "common/taxon_changelist.html"

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
                add_csv_taxon(list(data))
                msg = "Your itis taxon file has been successfully imported."
                self.message_user(request, msg, messages.SUCCESS)
            except:
                msg = (
                    "Something went wrong! "
                    "Please double check your file and try again."
                )
                self.message_user(request, msg, messages.ERROR)
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/taxon_csv_form.html", payload)


admin.site.register(Taxon, TaxonAdmin)
