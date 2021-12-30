from rest_framework import serializers
from activities.models import Property, Activity, Survey
from activities.enums import PropertyStatus


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

    class Meta:
        model = Activity
        fields = "__all__"


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = "__all__"
