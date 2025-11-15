
from django.urls import path

from users.views import UserTestAPIView, UserCreateAPIView, UpdateUserAPIView, ShowUserAPIView#, RemoveProfilePictureAPIView

urlpatterns = [
    path('test-api/', UserTestAPIView.as_view(), name='user-test'),
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('show-user/', ShowUserAPIView.as_view(), name='show-user'),
    path('update-user/', UpdateUserAPIView.as_view(), name='update-user'),
    # path('remove-profile-picture/', RemoveProfilePictureAPIView.as_view(), name='remove-profile-picture'),
]
