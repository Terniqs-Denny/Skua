# userauth/serializers/logout_serializer.py

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.utils import timezone

import jwt

from userauth.models import BlacklistedToken, UserSession
from userauth.utils.jwt_utils import decode_token


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        request = self.context.get("request")
        user = request.user

        # Extract access token and metadata
        access_token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        device_info = request.META.get('HTTP_USER_AGENT', 'Unknown Device')
        ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')

        if not access_token or not data["refresh"]:
            raise ValidationError("Both access and refresh tokens are required.")

        data["access_token"] = access_token
        data["device_info"] = device_info
        data["ip_address"] = ip_address

        # Check if refresh token is blacklisted
        if BlacklistedToken.objects.filter(token=data["refresh"]).exists():
            raise AuthenticationFailed("Refresh token has been blacklisted")

        try:
            payload = decode_token(data["refresh"])
        except jwt.ExpiredSignatureError:
            raise ValidationError("Refresh token expired.")
        except jwt.InvalidSignatureError:
            raise ValidationError("Invalid refresh token signature.")
        except jwt.InvalidTokenError:
            raise ValidationError("Invalid refresh token.")

        if payload.get("type") != "refresh":
            raise ValidationError("Invalid token type. Expected refresh token.")

        # Ensure the refresh token's user_id matches the authenticated user
        if str(payload.get("user_id")) != str(user.id):
            raise AuthenticationFailed("Token does not belong to the authenticated user.")

        return data
    

    def save(self, **kwargs):
        user = self.context["request"].user
        refresh_token = self.validated_data["refresh"]
        access_token = self.validated_data["access_token"]
        device_info = self.validated_data["device_info"]
        ip_address = self.validated_data["ip_address"]

        # Blacklist refresh token
        BlacklistedToken.objects.get_or_create(
            token=refresh_token,
            user=user,
            token_type="refresh"
        )

        # Blacklist access token if valid
        try:
            payload_access = decode_token(access_token)
            BlacklistedToken.objects.get_or_create(
                token=access_token,
                user=user,
                token_type="access"
            )
        except jwt.ExpiredSignatureError:
            pass
        except jwt.InvalidTokenError:
            raise ValidationError("Invalid access token.")

        # Update session
        try:
            session = UserSession.objects.get(
                user=user,
                refresh_token=refresh_token,
                device_info=device_info,
                is_active=True
            )
            session.is_active = False
            session.logout_at = timezone.now()
            session.last_activity = timezone.now()
            session.ip_address = ip_address
            session.save()
        except UserSession.DoesNotExist:
            pass  # Optional: Log this for auditing

        return {"message": "Successfully logged out."}

