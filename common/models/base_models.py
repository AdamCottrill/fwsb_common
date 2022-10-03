from django.db import models


class BaseModel(models.Model):
    """A base model that will be used by all of our other models that
    incldues a date created and date modified timestamp.
    """

    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LookupModel(BaseModel):
    """An abstarct base model for our lookup tables.  They wil inherit
    from our Base model, so they will get created_time and
    modified_time fields, but will also get standard fields 'abbrev',
    'label', 'slug', 'description', as well as a time stamp field that
    will flag when a record is no longer in use.  Methods depreciate
    and reactivate are available to toggle the state of a particular
    value.

    """

    id = models.AutoField(primary_key=True)
    obsolete_date = models.DateTimeField(blank=True, null=True)

    abbrev = models.CharField(max_length=2, unique=True, db_index=True)
    label = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    slug = models.SlugField(blank=False, unique=True, db_index=True, editable=False)

    class Meta:
        abstract = True
        ordering = ["abbrev"]

    def __str__(self):
        """String representation for a Cover object."""
        return f"{self.label}({self.abbrev})"

    def natural_key(self):
        return (self.abbrev,)

    def depreciate(self):

        self.obsolete_date = datetime.now()
        self.save()

    def reactivate(self):

        self.obsolete_date = None
        self.save()

    @property
    def is_active(self):
        return self.obsolete_date is None

    def save(self, *args, **kwargs):
        """
        Populate slug, centroid, and bounding box when we save the object.
        """
        self.slug = slugify(f"{self.label}-{self.slug}")
        super(LookupModel, self).save(*args, **kwargs)
