from django.db import models
from django.db.models import JSONField
# from core.mixins import AuditModelMixin

# If not specified, all fields are not null
# e.g.: text = models.TextField("text", null=True, blank=True)
class HasTimeStamp(models.Model):
    created = models.DateTimeField('date published', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)

    class Meta:
        abstract = True

class hasTitleStatus(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=35)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Property(HasTimeStamp, hasTitleStatus):
    address = models.TextField("text", blank=True)
    description = models.TextField("text", blank=True)
    disabled_at = models.DateTimeField('disabled at', null=True)

class Activity(HasTimeStamp, hasTitleStatus):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    schedule = models.DateTimeField('disabled at', auto_now=True)

class Survey(HasTimeStamp):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    answers = JSONField()
