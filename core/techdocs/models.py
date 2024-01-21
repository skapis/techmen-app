import uuid
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from app_settings.models import WorkList, WorkItemDescription


class ProductionLine(models.Model):
    lineId = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    lineName = models.CharField(max_length=255)
    lineSerialNumber = models.CharField(max_length=255, null=True)
    lineLocation = models.CharField(max_length=255, null=True)
    lineDate = models.DateField(null=True)
    valid = models.BooleanField(default=True)

    class Meta:
        ordering = ["lineName"]

    def __str__(self):
        return self.lineName


class Record(models.Model):
    recordId = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    internalId = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    lineCategory = models.ForeignKey(to=ProductionLine, on_delete=models.DO_NOTHING, null=True)
    date = models.DateField()
    transportPrice = models.DecimalField(max_digits=99, decimal_places=3, null=True)
    distance = models.IntegerField(null=True)
    created = models.DateTimeField(default=now)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True)
    workPrice = models.IntegerField(null=True)
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(default=now)
    confirmed_by = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.name


class MachineWorks(models.Model):
    workId = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    recordId = models.ForeignKey(to=Record, on_delete=models.CASCADE)
    workListItemName = models.CharField(max_length=255, null=True)
    workListItem = models.ForeignKey(to=WorkList, on_delete=models.DO_NOTHING, null=True)
    workDone = models.BooleanField(null=True)
    itemDesc = models.ForeignKey(to=WorkItemDescription, on_delete=models.DO_NOTHING, null=True)
    itemDescName = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = 'Machine work'
        ordering = ['workListItemName']

    def __str__(self):
        return f"{self.recordId} - {self.workListItem}"


class MachineIssues(models.Model):
    issueId = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    recordId = models.ForeignKey(to=Record, on_delete=models.CASCADE)
    issueName = models.CharField(max_length=255)
    fixed = models.BooleanField(default=False)
    fixTime = models.IntegerField(null=True)
    resolution = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Machine issues'
        ordering = ['issueName']

    def __str__(self):
        return self.issueName


class Components(models.Model):
    componentId = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    recordId = models.ForeignKey(to=Record, on_delete=models.CASCADE)
    componentSerialNumber = models.CharField(max_length=255)
    componentName = models.CharField(max_length=255)
    ordered = models.BooleanField(default=False)
    componentChange = models.CharField(max_length=255)
    componentPrice = models.DecimalField(max_digits=99, decimal_places=3, null=True)

    class Meta:
        verbose_name_plural = 'Components'
        ordering = ['componentName']

    def __str__(self):
        return self.componentName


class Variables(models.Model):
    variableId = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    variableName = models.CharField(max_length=255)
    value = models.IntegerField()
    unit = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Variables'

    def __str__(self):
        return self.variableName


class PriceOffer(models.Model):
    offerId = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    recordId = models.ForeignKey(to=Record, on_delete=models.CASCADE)
    offerDate = models.DateField(default=now)
    componentSerialNumber = models.CharField(max_length=255, null=True)
    workTime = models.IntegerField()
    componentPrice = models.DecimalField(max_digits=99, decimal_places=3, null=True)
    price = models.DecimalField(max_digits=99, decimal_places=3, null=True)

    def __str__(self):
        return f'{self.recordId.name}_{self.componentId.componentName}'


class RecordSum(models.Model):
    recordSumId = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    recordId = models.ForeignKey(to=Record, on_delete=models.CASCADE)
    workPriceSum = models.DecimalField(max_digits=99, decimal_places=3, null=True)
    componentPriceSum = models.DecimalField(max_digits=99, decimal_places=3, null=True)
    transportPriceSum = models.DecimalField(max_digits=99, decimal_places=3, null=True)
    total = models.DecimalField(max_digits=99, decimal_places=3, null=True)

    def __str__(self):
        return f"{self.recordId.name}"

