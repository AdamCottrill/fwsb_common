import pytest

from .common_factories import SpeciesFactory


from .common_factories import TaxonFactory
from ..models import Taxon


@pytest.fixture
def taxon_list():

    salmonidae = Taxon.add_root(
        instance=TaxonFactory.build(
            taxon="623286",
            itiscode=623286,
            taxon_name="Salmoninae",
            taxon_label="Salmoninae",
            taxonomic_rank="subfamily",
            vertinvert="vertebrate",
            omnr_provincial_code="070",
        )
    )

    oncorhynchus = salmonidae.add_child(
        instance=TaxonFactory.build(
            taxon="161974",
            itiscode=161974,
            taxon_name="Oncorhynchus",
            taxon_label="Pacific salmon",
            taxonomic_rank="genus",
            vertinvert="vertebrate",
            omnr_provincial_code="084",
        )
    )

    chinook = oncorhynchus.add_child(
        instance=TaxonFactory.build(
            taxon="161980",
            itiscode=161980,
            taxon_name="Oncorhynchus tshawytscha",
            taxon_label="Chinook salmon",
            taxonomic_rank="species",
            vertinvert="vertebrate",
            omnr_provincial_code="075",
        )
    )
    rainbow_trout = oncorhynchus.add_child(
        instance=TaxonFactory.build(
            taxon="161989",
            itiscode=161989,
            taxon_name="Oncorhynchus mykiss",
            taxon_label="rainbow trout",
            taxonomic_rank="species",
            vertinvert="vertebrate",
            omnr_provincial_code="076",
        )
    )

    salvelinus = salmonidae.add_child(
        instance=TaxonFactory.build(
            taxon="161999",
            itiscode=161999,
            taxon_name="Salvelinus",
            taxon_label="chars",
            taxonomic_rank="genus",
            vertinvert="vertebrate",
            omnr_provincial_code="086",
        )
    )

    lake_trout = salvelinus.add_child(
        instance=TaxonFactory.build(
            taxon="162002",
            itiscode=162002,
            taxon_name="Salvelinus namaycush",
            taxon_label="lake trout",
            taxonomic_rank="species",
            vertinvert="vertebrate",
            omnr_provincial_code="081",
        )
    )

    return [
        salmonidae,
        oncorhynchus,
        chinook,
        rainbow_trout,
        salvelinus,
        lake_trout,
    ]


@pytest.fixture
def species_list():

    whitefish = SpeciesFactory(
        spc="091", spc_nmco="lake whitefish", spc_nmsc="Coregonus clupeaformis"
    )

    perch = SpeciesFactory(
        spc="331", spc_nmco="Yellow Perch", spc_nmsc="Perca flavescens"
    )
    walleye = SpeciesFactory(spc="334", spc_nmco="walleye", spc_nmsc="Sander vitreum")

    return [whitefish, perch, walleye]
