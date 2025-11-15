# userauth/views/logout_view.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import logging

from userauth.utils.authentication import JWTAuthentication
from userauth.serializers import LogoutSerializer
from api.utils.response_wrapper import custom_exception_handler, error_response, success_response

logger = logging.getLogger(__name__)

class LogoutAPIView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = LogoutSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                result = serializer.save()
                return success_response(
                        data=None,
                        msg="Successfully logged out.",
                        status_code=status.HTTP_200_OK
                    )
            error_msg = next(iter(serializer.errors.values()))[0]
            return error_response(msg=error_msg, data=None, status_code=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.exception("Error in LogoutAPIView")
            context = {"view": self, "request": request}
            response = custom_exception_handler(e, context)
            return response
