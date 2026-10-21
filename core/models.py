import uuid
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class TimeStampedModel(models.Model):
    created_at = CreationDateTimeField(auto_now_add=True)
    updated_at = ModificationDateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimeStampedUUIDModel(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)

    class Meta:
        abstract = True
