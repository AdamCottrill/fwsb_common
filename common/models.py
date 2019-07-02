from django.db import models

#from django.contrib.gis.db import models
from django.template.defaultfilters import slugify


class BaseModel(models.Model):
    '''A base model that will be used by all of our other models that
incldues a date created and date modified timestamp.
    '''
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    obsolete = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Lake(BaseModel):
    """
    A lookup table for lakes.

    """

    abbrev = models.CharField(max_length=2, unique=True)
    lake_name = models.CharField(max_length=30, unique=True)

    #shoreline = models.MultiPolygonField(srid=4326, blank=True, null=True)
    #centroid = models.PointField(srid=4326)

    class Meta:
        ordering = ["abbrev"]

    def __str__(self):
        """ String representation for a lake."""
        return "{} ({})".format(self.lake_name, self.abbrev)

    def short_name(self):
        """The name of the lake without 'Lake ..'.

        A shorter verson of the lake name to save space when
        needed. THis may need to be turned into a property at some
        point.

        """
        return self.lake_name.replace('Lake ', '')


class ManagementUnit(BaseModel):
    """
    a class to hold geometries associated with arbirary ManagementUnits
    that can be represented as polygons.  Examples include quota
    management units and lake trout rehabilitation zones.  Used to find
    stocking events, cwts, and cwt recoveries occurred in (or
    potentially near) specific management Units.

    """

    label = models.CharField(max_length=25)
    slug = models.SlugField(blank=True, unique=True, editable=False)
    description = models.CharField(max_length=300)
    #geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    #centroid = models.PointField(srid=4326)
    lake = models.ForeignKey(Lake, default=1, on_delete=models.CASCADE)

    primary = models.BooleanField(
        "Primary management unit type for this jurisdiciton.",
        default=False,
        db_index=True,
    )

    MU_TYPE_CHOICES = (
        ("mu", "Management Unit"),
        ("ltrz", "Lake Trout Rehabilitation Zone"),
        ("qma", "Quota Management Area"),
        ("aa", "Assessment Area"),
        ("stat_dist", "Statistical District"),
    )

    mu_type = models.CharField(
        max_length=10, choices=MU_TYPE_CHOICES, default="mu")

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
        self.slug = self.get_slug()
        super(ManagementUnit, self).save(*args, **kwargs)


class Grid5(BaseModel):
    """'
    A lookup table for 5-minute grids within lakes.
    """

    grid = models.IntegerField()
    slug = models.SlugField(blank=False, unique=True, editable=False)
    #centroid = models.PointField(srid=4326)

    lake = models.ForeignKey(Lake, default=1, on_delete=models.CASCADE)

    class Meta:
        ordering = ["lake__abbrev", "grid"]

    def __str__(self):
        """ String representation for a 5-minute grid."""
        return "{:04d} ({})".format(self.grid, self.lake.abbrev)

    def get_slug(self):
        """
        the name is a concatenation of lake abbreviation, and the grid number.
        """
        lake = str(self.lake.abbrev)

        return slugify("{}_{:04d}".format(lake, self.grid))

    def save(self, *args, **kwargs):
        """
        Populate slug when we save the object.
        """
        # if not self.slug:
        self.slug = self.get_slug()
        super(Grid5, self).save(*args, **kwargs)


class Species(BaseModel):
    """A lookup table for species.  Note that both backcross and splake
    are considered species and not lake trout strains.  Field names
    follow fishnet naming conventions

    """

    abbrev = models.CharField(
        "US Abbreviation", max_length=5, blank=True, null=True)

    spc_nm = models.CharField(
        'Species Name', max_length=50, unique=True, blank=True, null=True)

    spc_nmco = models.CharField(
        'Official Common Name',
        max_length=50,
        unique=True,
        blank=True,
        null=True)

    spc_nmsc = models.CharField(
        'Scientific Name', max_length=50, blank=True, null=True)
    # family = models.CharField(max_length=50)
    spc = models.IntegerField(unique=True)

    spc_lab = models.CharField(max_length=10, unique=True)
    spc_nmfam = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Species"
        ordering = ["spc"]

    def __str__(self):
        """ String representation for a Species."""
        return "{} ({:03d})".format(self.spc_nmco.title(), self.spc)
