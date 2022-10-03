from django.contrib.gis.db import models
from django.contrib.gis.db.models import Q, UniqueConstraint

from django.template.defaultfilters import slugify

from .managers import Grid5Manager, LakeManager, ManagementUnitManager

from .base_models import BaseModel


class Lake(BaseModel):
    """
    A lookup table for lakes.

    """

    abbrev = models.CharField(max_length=2, unique=True, db_index=True)
    lake_name = models.CharField(max_length=30, unique=True)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    geom_ontario = models.MultiPolygonField(srid=4326, blank=True, null=True)

    centroid = models.PointField(srid=4326, blank=True, null=True)
    envelope = models.PolygonField(srid=4326, blank=True, null=True)

    centroid_ontario = models.PointField(srid=4326, blank=True, null=True)
    envelope_ontario = models.PolygonField(srid=4326, blank=True, null=True)

    objects = LakeManager()

    class Meta:
        ordering = ["abbrev"]

    def __str__(self):
        """String representation for a lake."""
        return "{} ({})".format(self.lake_name, self.abbrev)

    def natural_key(self):
        return (self.abbrev,)

    def short_name(self):
        """The name of the lake without 'Lake ..'.

        A shorter verson of the lake name to save space when
        needed. THis may need to be turned into a property at some
        point.

        """
        return self.lake_name.replace("Lake ", "")

    def save(self, *args, **kwargs):
        """
        Populate slug, centroid, and bounding box when we save the object.
        """
        # if not self.slug:

        if self.geom:
            self.centroid = self.geom.centroid
            self.envelope = self.geom.envelope

        if self.geom_ontario:
            self.centroid_ontario = self.geom_ontario.centroid
            self.envelope_ontario = self.geom_ontario.envelope

        super(Lake, self).save(*args, **kwargs)


class Grid5(BaseModel):
    """'
    A lookup table for 5-minute grids within lakes.
    """

    lake = models.ForeignKey(Lake, default=1, on_delete=models.CASCADE)

    grid = models.CharField(db_index=True, max_length=4)
    slug = models.SlugField(blank=False, unique=True, db_index=True, editable=False)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    centroid = models.PointField(srid=4326, blank=True, null=True)
    envelope = models.PolygonField(srid=4326, blank=True, null=True)

    objects = Grid5Manager()

    class Meta:
        ordering = ["lake__abbrev", "grid"]

    @property
    def grid0(self):
        return self.left_pad_grid()

    def left_pad_grid(self):
        """ """
        try:
            grid = "{:04d}".format(int(self.grid))
        except:
            grid = self.grid
        return grid

    def __str__(self):
        """String representation for a 5-minute grid."""

        grid = self.left_pad_grid()
        return "{} ({})".format(grid, self.lake.abbrev)

    def natural_key(self):
        return (self.lake__abbrev, self.grid)

    def get_slug(self):
        """
        the name is a concatenation of lake abbreviation, and the grid number.
        """
        lake = str(self.lake.abbrev)
        grid = self.left_pad_grid()
        return slugify("{}_{}".format(lake, grid))

    def save(self, *args, **kwargs):
        """
        Populate slug when we save the object.
        """
        # if not self.slug:
        self.slug = self.get_slug()

        if self.geom:
            self.centroid = self.geom.centroid
            self.envelope = self.geom.envelope

        super(Grid5, self).save(*args, **kwargs)


class ManagementUnitType(BaseModel):
    """A lookup table for management unit types.  Management units
    were originally a choice field in the ManagementUnit model, but
    moving them to a separate table allows us to dyamically add them
    in the admin and through the many-to-many relationship through
    ManagementUnitLake table, enforce a partial contstrain to ensure
    that there is only one 'primary' management unit type per lake.

    """

    abbrev = models.CharField(max_length=10, unique=True, db_index=True)
    label = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(blank=True, db_index=True, unique=True, editable=False)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "{} ({})".format(self.label, self.abbrev)

    def save(self, *args, **kwargs):
        """
        Populate slug when we save the object.
        """
        self.slug = slugify(self.abbrev)
        super(ManagementUnitType, self).save(*args, **kwargs)


class LakeManagementUnitType(BaseModel):
    """An association table (i.e. explict many-to-many) joining
    Management Unit Types to Lakes and ensuring that each lake can
    only have one 'primary' management unit and each management unit
    type can only appear within each lake once (A single lake cannot
    have two QMA management unit types)

    """

    lake = models.ForeignKey(Lake, default=1, on_delete=models.CASCADE)
    management_unit_type = models.ForeignKey(
        ManagementUnitType, default=1, on_delete=models.CASCADE
    )
    primary = models.BooleanField(
        "Primary management unit type for this lake.",
        default=False,
        db_index=True,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["lake"],
                condition=Q(primary=True),
                name="unique_lake_manunit_primary",
            ),
            UniqueConstraint(
                fields=["lake", "management_unit_type"],
                name="unique_lake_manunit_type",
            ),
        ]

    def __str__(self):
        return "{}-{}".format(self.lake.abbrev, self.management_unit_type.abbrev)


class ManagementUnit(BaseModel):
    """
    a class to hold geometries associated with arbirary ManagementUnits
    that can be represented as polygons.  Examples include quota
    management units and lake trout rehabilitation zones.  Used to find
    stocking events, cwts, and cwt recoveries occurred in (or
    potentially near) specific management Units.

    """

    # move
    lake = models.ForeignKey(Lake, default=1, on_delete=models.CASCADE)

    lake_management_unit_type = models.ForeignKey(
        LakeManagementUnitType, on_delete=models.CASCADE
    )

    grids = models.ManyToManyField(Grid5)

    label = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(blank=True, db_index=True, unique=True, editable=False)
    description = models.CharField(max_length=1000)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    centroid = models.PointField(srid=4326, blank=True, null=True)
    envelope = models.PolygonField(srid=4326, blank=True, null=True)

    objects = ManagementUnitManager()

    class Meta:
        ordering = ["lake__abbrev", "label"]

    def get_slug(self):
        """
        the name is a concatenation of lake abbreviation, the managemnet unit
        type and and the management unit label.
        """

        lake = str(self.lake.abbrev)
        mu_type = self.lake_management_unit_type.management_unit_type.abbrev

        return slugify("_".join([lake, mu_type, self.label]))

    def name(self):
        """
        returns the name of the managment unit including the lake it
        is associated with, the management unit type and the label

        """
        mu_type = self.lake_management_unit_type.management_unit_type.abbrev
        return " ".join([str(self.lake.abbrev), mu_type.upper(), self.label])

    def __str__(self):
        return self.name()

    def save(self, *args, **kwargs):
        """
        Populate slug when we save the object.
        """
        # if not self.slug:

        if self.geom:
            self.centroid = self.geom.centroid
            self.envelope = self.geom.envelope

        self.slug = self.get_slug()
        super(ManagementUnit, self).save(*args, **kwargs)
