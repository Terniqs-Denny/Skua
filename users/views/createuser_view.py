# users/views/createuser_view.py

import logging
from rest_framework.views import APIView
from rest_framework import status

from users.serializers import UserCreateSerializer
from api.utils import success_response, error_response ,custom_exception_handler

logger = logging.getLogger(__name__)
class UserCreateAPIView(APIView):
    def post(self, request):
        try:
            serializer = UserCreateSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                return success_response(
                    data={"user_id": str(user.id)},
                    msg="User created successfully",
                    status_code=status.HTTP_201_CREATED
                )
            
            error_msg = next(iter(serializer.errors.values()))[0]

            return error_response(
                msg=error_msg,
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger.exception("Error in UserCreateAPIView")
            context = {"view": self, "request": request}
            response = custom_exception_handler(e, context)
            return response
