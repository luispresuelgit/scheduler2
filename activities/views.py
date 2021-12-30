from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from activities.models import Property, Activity, Survey
from activities.serializers import PropertySerializer, ActivitySerializer, SurveySerializer
from activities.enums import PropertyStatus
from django.utils import timezone
from activities.exceptions import DisabledPropertyError, SameDateHourError
from django.http import JsonResponse

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
def property_detail(request, pk):
    """
    Retrieve, update or delete an property.
    """
    try:
        property = Property.objects.get(pk=pk)
    except property.DoesNotExist:
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
    List all Activities, or create a new activity.
    """
    if request.method == 'GET':
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # will automatically return the first object that meets this condition
        # if not found will return None
        property_disabled = Property.objects.filter(status=PropertyStatus.disabled.name).first()
        if property_disabled is not None:
            raise DisabledPropertyError()

        # import pdb
        # pdb.set_trace()

        data = JSONParser().parse(request)
        property = Property.objects.get(id=data['property_id'])
        new_activity = Activity(
            title=data['title'],
            schedule=data['schedule'],
            property=property
        )
        new_activity.save()
        serializer = ActivitySerializer(new_activity)
        return JsonResponse(serializer.data, status=201)


@csrf_exempt
def activity_detail(request, pk):
    """
    Retrieve, update or delete an activity.
    """
    try:
        activity = Activity.objects.get(pk=pk)
    except activity.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ActivitySerializer(activity)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ActivitySerializer(activity, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        activity.delete()
        return HttpResponse(status=204)

@csrf_exempt
def survey_list(request):
    """
    List all Surveys, or create a new survey.
    """
    if request.method == 'GET':
        surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SurveySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def survey_detail(request, pk):
    """
    Retrieve, update or delete an survey.
    """
    try:
        survey = Activity.objects.get(pk=pk)
    except survey.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SurveySerializer(survey)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        if data['status'] == 'disabled':
            data['disabled_at'] = timezone.now()
        else:
            data['disabled_at'] = None
        serializer = PropertySerializer(survey, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        survey.delete()
        return HttpResponse(status=204)
