from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from rbac_auth.contrib.rest_framework.mixins import DestroyModelMixin


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        abstract = True

class ArchivableModelMixin(DestroyModelMixin, models.Model):
    archived = models.BooleanField(default=False)

    class Meta:
        abstract = True

class SluggedModelMixin(models.Model):
    __slugged_field = 'name'
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        slugged = getattr(self, self.__slugged_field)
        self.slug = slugify(slugged)
        super(SluggedModelMixin, self).save(*args, **kwargs)
