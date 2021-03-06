# from django.db import models
from django.contrib.gis.db import models

# from django.contrib.gis.db import models
from django.template.defaultfilters import slugify


class BaseModel(models.Model):
    """A base model that will be used by all of our other models that
incldues a date created and date modified timestamp.
    """

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
        """ String representation for a lake."""
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

    def left_pad_grid(self):
        """
        """
        try:
            grid = "{:04d}".format(int(self.grid))
        except:
            grid = self.grid
        return grid

    def __str__(self):
        """ String representation for a 5-minute grid."""

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


class ManagementUnit(BaseModel):
    """
    a class to hold geometries associated with arbirary ManagementUnits
    that can be represented as polygons.  Examples include quota
    management units and lake trout rehabilitation zones.  Used to find
    stocking events, cwts, and cwt recoveries occurred in (or
    potentially near) specific management Units.

    """

    lake = models.ForeignKey(Lake, default=1, on_delete=models.CASCADE)

    label = models.CharField(max_length=25, db_index=True)
    slug = models.SlugField(blank=True, db_index=True, unique=True, editable=False)
    description = models.CharField(max_length=300)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    centroid = models.PointField(srid=4326, blank=True, null=True)
    envelope = models.PolygonField(srid=4326, blank=True, null=True)

    primary = models.BooleanField(
        "Primary management unit type for this jurisdiciton.",
        default=False,
        db_index=True,
    )

    MU_TYPE_CHOICES = (
        ("mu", "Management Unit"),
        ("ltrz", "Lake Trout Rehabilitation Zone"),
        ("bltrz", "Buffered Lake Trout Rehabilitation Zone"),
        ("qma", "Quota Management Area"),
        ("aa", "Assessment Area"),
        ("area", "Area"),
        ("subarea", "Assessment Area"),
        ("stat_dist", "Statistical District"),
        ("moe", "MOE Block"),
        ("basin", "Basin"),
        ("naz", "Nearshore Assessment Zone"),
        ("grid10", "10-Minute Grid"),
        ("region", "Region"),
    )

    mu_type = models.CharField(max_length=10, choices=MU_TYPE_CHOICES, default="mu")

    grids = models.ManyToManyField(Grid5)

    objects = ManagementUnitManager()

    class Meta:
        ordering = ["lake__abbrev", "mu_type", "label"]

    def get_slug(self):
        """
        the name is a concatenation of lake abbreviation, the managemnet unit
        type and and the management unit label.
        """

        lake = str(self.lake.abbrev)

        return slugify("_".join([lake, self.mu_type, self.label]))

    def name(self):
        """
        returns the name of the managment unit including the lake it
        is associated with, the management unit type and the label

        """
        return " ".join([str(self.lake), self.mu_type.upper(), self.label])

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


class Species(BaseModel):
    """A lookup table for species.  Note that both backcross and splake
    are considered species and not lake trout strains.  Field names
    follow fishnet naming conventions

    """

    spc = models.CharField(max_length=3, unique=True, db_index=True)

    abbrev = models.CharField("US Abbreviation", max_length=5, blank=True, null=True)

    spc_nm = models.CharField("Species Name", max_length=50, blank=True, null=True)

    spc_nmco = models.CharField(
        "Official Common Name", max_length=50, blank=True, null=True
    )

    spc_nmsc = models.CharField("Scientific Name", max_length=50, blank=True, null=True)

    spc_lab = models.CharField(max_length=10)
    spc_nmfam = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    royalty_flag = models.BooleanField(default=False)
    quota_flag = models.BooleanField(default=False)

    objects = SpeciesManager()

    class Meta:
        verbose_name_plural = "Species"
        ordering = ["spc"]

    def __str__(self):
        """ String representation for a Species."""

        if self.spc_nmco is not None:
            return "{} ({})".format(self.spc_nmco.title(), self.spc)
        else:
            return "{} ({})".format(self.spc_nmsc, self.spc)

    def natural_key(self):
        return (self.abbrev,)
