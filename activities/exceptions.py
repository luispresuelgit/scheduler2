from rest_framework.exceptions import APIException


class DisabledPropertyError(APIException):
    status_code = 400
    default_code = "disabled_prop_error"
    default_detail = "Cannot create activities if a property is disabled"


class SameDateHourError(APIException):
    status_code = 400
    default_detail = "Cannot create activities within same property"
    default_code = "same_date_hour_error"