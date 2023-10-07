import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('дата изменения'))

    class Meta:
        abstract = True
