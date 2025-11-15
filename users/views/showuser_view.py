
import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from api.utils.response_wrapper import custom_exception_handler, success_response, error_response
from users.serializers import ShowUserSerializer, ShowUserValidateSerializer
from userauth.utils.authentication import JWTAuthentication

logger = logging.getLogger(__name__)

class ShowUserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            query_serializer = ShowUserValidateSerializer(data=request.GET, context={"request": request})

            if not query_serializer.is_valid():
                error_msg = next(iter(query_serializer.errors.values()))[0]
                return error_response(
                    msg=error_msg,
                    data=None,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            user = query_serializer.validated_data['user_id']
            
            serializer = ShowUserSerializer(user)

            return success_response(
                data=serializer.data,
                msg="User fetched",
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception("Error in ShowUserAPIView")
            context = {"view": self, "request": request}
            response = custom_exception_handler(e, context)
            return response