from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from treebeard.mp_tree import MP_Node

from .base_models import BaseModel
from .managers import SpeciesManager


class BaseTreeModel(MP_Node):
    """A base model that will be used by all of our other models that
    incldues a date created and date modified timestamp.
    """

    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Taxon(BaseTreeModel):
    """A lookup table for taxon - used for non-fish and diet data.
    Taxon will contain an optional foreign key to species where that is appropraite.

    """

    # spc  optional foreign key to Species

    TAXON_RANK_CHOICES = (
        ("other", "Other"),
        ("domain", "Domain"),
        ("kingdom", "Kingdom"),
        ("subkingdom", "Subkingdom"),
        ("infrakingdom", "Infrakingdom"),
        ("superphylum", "Superphylum"),
        ("phylum", "Phylum"),
        ("infraphylum", "Infraphylum"),
        ("subphylum", "Subphylum"),
        ("class", "Class"),
        ("subclass", "Subclass"),
        ("superclass", "Superclass"),
        ("infraclass", "Infraclass"),
        ("order", "Order"),
        ("infraorder", "Infraorder"),
        ("suborder", "Suborder"),
        ("superorder", "Superorder"),
        ("genus", "Genus"),
        ("subgenus", "Subgenus"),
        ("family", "Family"),
        ("superfamily", "Superfamily"),
        ("subfamily", "Subfamily"),
        ("tribe", "Tribe"),
        ("species", "Species"),
    )

    taxon = models.CharField(max_length=10, unique=True, db_index=True)
    itiscode = models.CharField(
        "ITIS TSN", max_length=10, unique=True, db_index=True, blank=True, null=True
    )

    taxon_name = models.CharField(
        "Scientific Name", max_length=100, blank=True, null=True
    )
    taxon_label = models.CharField("Common Name", max_length=100, blank=True, null=True)
    taxonomic_rank = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        choices=TAXON_RANK_CHOICES,
        default="species",
    )

    VERTINVERT_CHOICES = [
        ("other", "Other"),
        ("plant", "Plant"),
        ("invertebrate", "Invertebrate"),
        ("vertebrate", "Vertebrate"),
    ]

    vertinvert = models.CharField(
        max_length=12, choices=VERTINVERT_CHOICES, default="invertebrate"
    )
    omnr_provincial_code = models.CharField(
        "HHFAU Code", max_length=4, unique=True, db_index=True, blank=True, null=True
    )
    # codetype

    class Meta:

        ordering = ["taxon"]

    def __str__(self):
        """String representation for a taxon."""

        name = self.taxon_name if self.taxon_name else self.taxon_label

        return "{} (taxon = {})".format(name.title(), self.taxon)

    def natural_key(self):
        return (self.taxon,)


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

    flen_min = models.FloatField(
        "Minimum Fork Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(700)],
    )
    flen_max = models.FloatField(
        "Maximim Fork Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(2000)],
    )
    tlen_min = models.FloatField(
        "Minimum Total Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(700)],
    )
    tlen_max = models.FloatField(
        "Maximum Total Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(2000)],
    )
    rwt_min = models.FloatField(
        "Minimum Round Weight (g)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(5000)],
    )
    rwt_max = models.FloatField(
        "Maximum Round Weight (g)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(5000)],
    )
    k_min_error = models.FloatField(
        "Minimum K (TLEN) - error",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(2.0)],
    )
    k_min_warn = models.FloatField(
        "Minimum K (TLEN) - warning",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1.5)],
    )
    k_max_error = models.FloatField(
        "Maximum K (FLEN) - error",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(5.0)],
    )
    k_max_warn = models.FloatField(
        "Maximum K (FLEN) - warning",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(4.0)],
    )
    flen2tlen_alpha = models.FloatField(
        "Intercept of FLEN-TLEN Regression",
        blank=True,
        null=True,
        validators=[MinValueValidator(-20.0), MaxValueValidator(80.0)],
    )
    flen2tlen_beta = models.FloatField(
        "Slope of FLEN-TLEN Regression",
        blank=True,
        null=True,
        validators=[MinValueValidator(1.0), MaxValueValidator(1.25)],
    )

    objects = SpeciesManager()

    class Meta:
        verbose_name_plural = "Species"
        ordering = ["spc"]

    def __str__(self):
        """String representation for a Species."""

        if self.spc_nmco is not None:
            return "{} ({})".format(self.spc_nmco.title(), self.spc)
        else:
            return "{} ({})".format(self.spc_nmsc, self.spc)

    def natural_key(self):
        return (self.abbrev,)
