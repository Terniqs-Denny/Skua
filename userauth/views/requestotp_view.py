# userauth/views/requestotp_view.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

import logging

from userauth.serializers import OTPRequestSerializer
from api.utils.response_wrapper import custom_exception_handler, error_response, success_response

logger = logging.getLogger(__name__)

class RequestOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = OTPRequestSerializer(data=request.data)
            if serializer.is_valid():
                otp_data = serializer.save()

                logger.info(f"OTP generated for {otp_data['channel']}: {otp_data['code']}")
                
                return success_response(
                    data={
                        "user_id": otp_data["user_id"],
                        "expires_at": otp_data["expires_at"].isoformat()
                    },
                    msg=f"OTP sent to your {otp_data['channel']}",
                    status_code=status.HTTP_201_CREATED
                )
            error_msg = next(iter(serializer.errors.values()))[0]
            return  error_response(
                msg=error_msg,
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger.exception("Error in RequestOTPAPIView")
            context = {"view": self, "request": request}
            response = custom_exception_handler(e, context)
            return response


