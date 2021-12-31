from rest_framework import serializers
from activities.models import Property, Activity, Survey
from activities.enums import PropertyStatus, ActivityStatus
from django.utils import timezone
from django.http import HttpRequest


class PropertySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    address = serializers.CharField()
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=PropertyStatus.choices(), default='enabled')
    disabled_at = serializers.DateTimeField(required=False, allow_null=True, default=None)

    def create(self, validated_data):
        """
        Create and return a new `Property` instance, given the validated data.
        """
        return Property.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Property` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.address = validated_data.get('address', instance.address)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.disabled_at = validated_data.get('disabled_at', instance.disabled_at)
        instance.save()
        return instance


class ActivitySerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    condition = serializers.SerializerMethodField('get_condition')
    survey = serializers.SerializerMethodField('get_survey')

    class Meta:
        model = Activity
        fields = "__all__"

    def get_condition(self, activity):
        condition = "N/A"
        if activity.status == ActivityStatus.active.name and activity.schedule >= timezone.now():
            condition = "Pending"

        if activity.status == ActivityStatus.active.name and activity.schedule < timezone.now():
            condition = "Delayed"

        if activity.status == ActivityStatus.done.name:
            condition = "Finalized"
        return condition

    def get_survey(self, activity):
        survey_url = "Not created yet"
        survey = Survey.objects.filter(activity_id=activity.id).first()
        if survey is not None:
            request = HttpRequest()
            # base_url = request.get_host()
            ip = '127.0.0.1'
            base_url = ip
            port = '8000'
            if port:
                base_url += ':%s' % port
            survey_url = 'http://%s/activities/%s/survey/%s' % (base_url, activity.id, survey.id)
        return survey_url


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = "__all__"
