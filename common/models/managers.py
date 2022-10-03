"""
"""


from django.db import models


class LakeManager(models.Manager):
    """A custom manager for our lake objects that excludes geometry
    objects by default - they tend to be very expensive to include in
    queries unless required."""

    def get_queryset(self, *args, **kwargs):
        return (
            super(LakeManager, self)
            .get_queryset(*args, **kwargs)
            .defer(
                "geom",
                "geom_ontario",
                "envelope",
                "envelope_ontario",
                "centroid",
                "centroid_ontario",
            )
        )

    def get_by_natural_key(self, abbrev):
        return self.get(abbrev=abbrev)


class Grid5Manager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super(Grid5Manager, self)
            .get_queryset(*args, **kwargs)
            .defer("geom", "envelope", "centroid")
        )

    def get_by_natural_key(self, lake, grid):
        return self.get(lake__abbrev=lake, grid=grid)


class ManagementUnitManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super(ManagementUnitManager, self)
            .get_queryset(*args, **kwargs)
            .defer("geom", "envelope", "centroid")
        )


class SpeciesManager(models.Manager):
    def get_by_natural_key(self, spc):
        return self.get(spc=spc)


class LookupManager(models.Manager):
    """A custom model manager for lookup tables - only returns those
    objects that are currently active (obsolete_date is null).
    Records with obssolete_date populated are not returned by default.

    """

    def get_queryset(self):
        "return only those records where the obsolete date is null."
        return super().get_queryset().filter(obsolete_date__isnull=True)

    def get_by_natural_key(self, abbrev):
        return self.get(abbrev=abbrev)
