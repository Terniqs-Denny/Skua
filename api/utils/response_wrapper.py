
from rest_framework.response import Response
from rest_framework.views import exception_handler

def success_response(data=None, msg="", status_code=200):
    return Response({
        "msg": msg,
        "data": data if data is not None else {}
    }, status=status_code)

def error_response(msg, status_code=400, data=None):
    return Response({
        "msg": msg,
        "data": data if data is not None else {}
    }, status=status_code)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        msg = str(exc.detail) if hasattr(exc, 'detail') else str(exc)
        return error_response(msg, status_code=response.status_code)

    return error_response("Internal server error", status_code=500)
