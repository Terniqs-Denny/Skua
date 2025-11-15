
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging

from api.utils.response_wrapper import custom_exception_handler, error_response, success_response
from users.serializers import UpdateUserSerializer
from userauth.utils.authentication import JWTAuthentication

logger = logging.getLogger(__name__)

class UpdateUserAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            serializer = UpdateUserSerializer(data=request.data, context={"request": request})

            if serializer.is_valid():
                user = serializer.update(validated_data=serializer.validated_data)
                
                return success_response(
                    data={"user_id": str(user.id)},
                    msg="User profile updated successfully",
                    status_code=status.HTTP_201_CREATED
                )

            error_msg = next(iter(serializer.errors.values()))[0]

            return error_response(
                msg=error_msg,
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
        except Exception as e:
            logger.exception("Error in UpdateUserAPIView")
            context = {"view": self, "request": request}
            response = custom_exception_handler(e, context)
            return response
