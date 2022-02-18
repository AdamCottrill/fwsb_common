import pytest

from .common_factories import SpeciesFactory


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
