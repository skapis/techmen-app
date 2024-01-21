import uuid
from django.db import models


class WorkList(models.Model):
    itemId = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    valid = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Work list'
        ordering = ["name"]

    def __str__(self):
        return self.name


class WorkItemDescription(models.Model):
    workItemDescId = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    valid = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
