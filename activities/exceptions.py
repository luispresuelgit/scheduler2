from rest_framework.exceptions import APIException


class DisabledPropertyError(APIException):
    status_code = 400
    default_code = "disabled_prop_error"
    default_detail = "Cannot create activities if a property is disabled"


class SameDateHourError(APIException):
    status_code = 400
    default_detail = "Cannot schedule activities at the same time with the same property"
    default_code = "same_date_hour_error"


class CannotRescheduleCanceledError(APIException):
    status_code = 400
    default_detail = "Cannot reschedule canceled activities"
    default_code = "cannot_reschedule_cancelled_error"


class DataNotSupportedError(APIException):
    status_code = 400
    default_detail = "not supported data passed at request"
    default_code = "not_supported_data_error"