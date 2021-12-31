from django.db import models
from django.db.models import JSONField
from activities.enums import PropertyStatus, ActivityStatus

# If not specified, all fields are not null
# e.g.: text = models.TextField("text", null=True, blank=True)


class HasCreatedTimeStamp(models.Model):
    created_at = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        abstract = True


class HasUpdatedTimeStamp(models.Model):
    updated_at = models.DateTimeField('date modified', auto_now=True)

    class Meta:
        abstract = True


class hasTitleStatus(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=35)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Property(HasCreatedTimeStamp, HasUpdatedTimeStamp, hasTitleStatus):
    address = models.TextField("text", blank=True)
    description = models.TextField("text", blank=True)
    disabled_at = models.DateTimeField('disabled at', null=True)
    status = models.CharField(max_length=35, choices=PropertyStatus.choices(), default='enabled')


class Activity(HasCreatedTimeStamp, HasUpdatedTimeStamp, hasTitleStatus):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    schedule = models.DateTimeField('schedule')
    status = models.CharField(max_length=35, choices=ActivityStatus.choices(), default='active')


class Survey(HasCreatedTimeStamp):
    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE
    )
    answers = JSONField()
