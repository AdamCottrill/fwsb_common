from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .managers import SpeciesManager
from .base_models import BaseModel


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
