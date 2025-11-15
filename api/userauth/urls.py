# api/userauth/urls.py

from django.urls import path
from userauth.views import RequestOTPAPIView, VerifyOTPAPIView, RefreshTokenAPIView, LogoutAPIView

urlpatterns = [
    path('req-otp/', RequestOTPAPIView.as_view(), name='request-otp'),
    path("verify-otp/", VerifyOTPAPIView.as_view(), name="verify-otp"),
    path("refresh-token/", RefreshTokenAPIView.as_view(), name="refresh-token"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]