
import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.utils.response_wrapper import custom_exception_handler, error_response, success_response
from userauth.serializers import VerifyOTPSerializer

logger = logging.getLogger(__name__)

class VerifyOTPAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = VerifyOTPSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                token_data = serializer.save()

                return success_response(
                    data={
                        "access": token_data['access'],
                        "refresh": token_data['refresh'],
                        "user_id": token_data['user_id'],
                        "session_id": token_data['session_id']
                    },
                    msg="OTP verified",
                    status_code=status.HTTP_200_OK
                )

            error_msg = next(iter(serializer.errors.values()))[0]
            return error_response(msg=error_msg, data=None, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Error in VerifyOTPAPIView")
            context = {"view": self, "request": request}
            response = custom_exception_handler(e, context)
            return response
