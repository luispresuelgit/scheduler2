# custom handler
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    import pdb
    pdb.set_trace()
    response = exception_handler(exc, context)
    if isinstance(exc, DisabledPropertyError):
        # response.data['status_code'] = DisabledPropertyError.status_code
        # response.data['default_code'] = DisabledPropertyError.default_code
        # response.data['default_detail'] = DisabledPropertyError.default_detail
        response.data = {}
        response.data['error'] = str(exc)

    if response is not None:
        response.data['status_code'] = response.status_code

        # replace detail key with message key by delete detail key
        response.data['message'] = response.data['detail']
        del response.data['detail']