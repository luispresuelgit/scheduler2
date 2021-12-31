from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from rest_framework.parsers import JSONParser
from activities.models import Property, Activity, Survey
from activities.serializers import PropertySerializer, ActivitySerializer, SurveySerializer
from activities.enums import PropertyStatus, ActivityStatus
from django.utils import timezone
from activities.exceptions import (
    DisabledPropertyError, SameDateHourError, CannotRescheduleCanceledError,
    DataNotSupportedError
)
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware


def index(request):
    return HttpResponse("Hello, world. You're at the activities2 index.")


@csrf_exempt
def property_list(request):
    """
    List all code Properties, or create a new property.
    """
    if request.method == 'GET':
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if data['status'] == 'disabled':
            data['disabled_at'] = timezone.now()
        serializer = PropertySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def property_detail(request, property_id):
    """
    Retrieve, update or delete an property.
    """
    try:
        property = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PropertySerializer(property)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        if data['status'] == 'disabled':
            data['disabled_at'] = timezone.now()
        else:
            data['disabled_at'] = None
        serializer = PropertySerializer(property, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        property.delete()
        return HttpResponse(status=204)


@csrf_exempt
def activity_list(request):
    """
    List all Activities.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        if len(data.keys()) == 0:
            three_days_ago = timezone.now() - timezone.timedelta(days=3)
            two_weeks_ahead = timezone.now() + timezone.timedelta(days=14)
            activities = Activity.objects.filter(schedule__range=[three_days_ago, two_weeks_ahead]).all()
            serializer = ActivitySerializer(activities, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            msg = {
                "code": DataNotSupportedError.default_code,
                "message": DataNotSupportedError.default_detail
            }
            if 'status' in data.keys():
                if 'date_init' in data.keys():
                    if len(data.keys()) != 3:
                        if 'date_end' not in data.keys():
                            extra = " - missing: 'date_end' attribute"
                            msg['message'] += extra
                        return JsonResponse(msg, status=DataNotSupportedError.status_code)
                if 'date_end' in data.keys():
                    if len(data.keys()) != 3:
                        if 'date_init' not in data.keys():
                            extra = " - missing: 'date_init' attribute"
                            msg['message'] += extra
                        return JsonResponse(msg, status=DataNotSupportedError.status_code)
                if len(data.keys()) > 1:
                    return JsonResponse(msg, status=DataNotSupportedError.status_code)
            elif 'date_init' in data.keys():
                if len(data.keys()) != 2:
                    if 'date_end' not in data.keys():
                        extra = " - missing: 'date_end' attribute"
                        msg['message'] += extra
                    return JsonResponse(msg, status=DataNotSupportedError.status_code)
            elif 'date_end' in data.keys():
                if len(data.keys()) != 2:
                    if 'date_init' not in data.keys():
                        extra = " - missing: 'date_init' attribute"
                        msg['message'] += extra
                    return JsonResponse(msg, status=DataNotSupportedError.status_code)

            query = Activity.objects
            if 'status' in data.keys():
                query = query.filter(status=data['status'])
            if 'date_init' in data.keys() and 'date_end' in data.keys():
                date_init = data['date_init']
                date_end = data['date_end']
                query = query.filter(schedule__range=[date_init, date_end])
            activities = query.all()
            serializer = ActivitySerializer(activities, many=True)
            return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def activity_create(request):
    """
    Create Activities.
    """
    if request.method == 'POST':
        # will automatically return the first object that meets this condition
        # if not found will return None
        property_disabled = Property.objects.filter(status=PropertyStatus.disabled.name).first()
        if property_disabled is not None:
            msg = {"code": DisabledPropertyError.default_code, "message": DisabledPropertyError.default_detail}
            return JsonResponse(msg, status=DisabledPropertyError.status_code)

        data = JSONParser().parse(request)

        date_hour_init = make_aware(parse_datetime(data['schedule']))
        hour_head = date_hour_init + timezone.timedelta(hours=1)
        query = Activity.objects.filter(schedule__range=[date_hour_init, hour_head])
        query = query.filter(property_id=data['property_id'])
        activities = query.all()
        if len(activities) > 0:
            msg = {"code": SameDateHourError.default_code, "message": SameDateHourError.default_detail}
            return JsonResponse(msg, status=SameDateHourError.status_code)

        property = Property.objects.get(id=data['property_id'])
        new_activity = Activity(
            title=data['title'],
            schedule=data['schedule'],
            status=data['status'] if 'status' in data.keys() else ActivityStatus.active.name,
            property=property
        )
        new_activity.save()
        serializer = ActivitySerializer(new_activity)
        return JsonResponse(serializer.data, status=201)


@csrf_exempt
def activity_detail(request, activity_id):
    """
    Retrieve, update or delete an activity.
    """
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return HttpResponse(status=404)

    msg = {
        "code": DataNotSupportedError.default_code,
        "message": DataNotSupportedError.default_detail
    }
    if request.method == 'GET':
        serializer = ActivitySerializer(activity)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        if 'schedule' not in data.keys() or len(data.keys()) > 1:
            return JsonResponse(msg, status=DataNotSupportedError.status_code)

        if activity.status == ActivityStatus.cancelled.name:
            msg = {
                "code": CannotRescheduleCanceledError.default_code,
                "message": CannotRescheduleCanceledError.default_detail
            }
            return JsonResponse(msg, status=CannotRescheduleCanceledError.status_code)

        activity.schedule = make_aware(parse_datetime(data['schedule']))
        activity.save()
        serializer = ActivitySerializer(activity)
        return JsonResponse(serializer.data, status=201)

    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        if 'status' not in data.keys() or len(data.keys()) > 1:
            return JsonResponse(msg, status=DataNotSupportedError.status_code)
        activity.status = data['status']
        activity.save()
        serializer = ActivitySerializer(activity)
        return JsonResponse(serializer.data, status=201)


@csrf_exempt
def survey_list(request, activity_id):
    """
    List all Surveys, or create a new survey.
    """
    if request.method == 'GET':
        surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        activity = Activity.objects.get(id=activity_id)
        new_survey = Survey(
            created_at=timezone.now(),
            answers=data['answers'],
            activity=activity
        )
        try:
            new_survey.save()
        except IntegrityError as e:
            content = {'error': str(e.__cause__)}
            return JsonResponse(content, status=400)
        serializer = SurveySerializer(new_survey)
        return JsonResponse(serializer.data, status=201)


@csrf_exempt
def survey_detail(request, activity_id, survey_id):
    """
    Retrieve, update or delete an survey.
    """
    try:
        survey = Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SurveySerializer(survey)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        survey.answers = data['answers']
        survey.save()
        serializer = SurveySerializer(survey)
        return JsonResponse(serializer.data, status=201)

    elif request.method == 'DELETE':
        survey.delete()
        return HttpResponse(status=204)
