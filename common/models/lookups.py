"""models that represent lookup tables that are used by all GLIS
applications. (these could be split into categories some day based on
type of information they contains - age info, tag attributes, habitat,
etc.)

"""

from datetime import datetime
from django.db import models
from django.utils.text import slugify
from .base_models import LookupModel
from .managers import LookupManager


class CoverType(LookupModel):
    """A lookup table for habitat cover types."""

    all_objects = models.Manager()
    objects = LookupManager()


class BottomType(LookupModel):
    """A lookup table for Bottom types."""

    all_objects = models.Manager()
    objects = LookupManager()
