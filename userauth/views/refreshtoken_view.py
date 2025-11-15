# userauth/views/refreshtoken_view.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

import logging

from userauth.serializers import RefreshTokenSerializer
from api.utils.response_wrapper import custom_exception_handler, error_response, success_response

logger = logging.getLogger(__name__)

class RefreshTokenAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = RefreshTokenSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                tokens = serializer.save()
                return success_response(
                    data={
                        "access": tokens['access'],
                        "refresh": tokens['refresh']
                    },
                    msg="Token refreshed successfully.",
                    status_code=status.HTTP_200_OK
                )
            error_msg = next(iter(serializer.errors.values()))[0]
            return error_response(msg=error_msg, data=None, status_code=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Error in RefreshTokenAPIView")
            context = {"view": self, "request": request}
            response = custom_exception_handler(e, context)
            return response
