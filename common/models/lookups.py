"""models that represent lookup tables that are used by all GLIS
applications. (these could be split into categories some day based on
type of information they contains - age info, tag attributes, habitat,
etc.)

"""


from django.db import models

from .base_models import LookupModel
from .managers import LookupManager


class Vessel(LookupModel):
    """A lookup table for our vessels.  Attributes 'abbrev' and
    'label' may not be ideal, but it is workable for today."""

    #override the abbrev field to increase its size
    abbrev = models.CharField(max_length=6, unique=True, db_index=True)

    all_objects = models.Manager()
    objects = LookupManager()



class CoverType(LookupModel):
    """A lookup table for habitat cover types."""

    all_objects = models.Manager()
    objects = LookupManager()


class BottomType(LookupModel):
    """A lookup table for Bottom types."""

    all_objects = models.Manager()
    objects = LookupManager()
