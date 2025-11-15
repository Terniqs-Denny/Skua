# userauth/serializers/refreshtoken_serializer.py

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone

import logging
import jwt

from userauth.models import UserSession, BlacklistedToken
from users.models import User
from userauth.utils.jwt_utils import generate_tokens, decode_token

logger = logging.getLogger(__name__)
class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        request = self.context['request']
        refresh_token = attrs['refresh']
        access_token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
        device_info = request.META.get('HTTP_USER_AGENT', 'Unknown Device')
        ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')

        # Check blacklist
        if BlacklistedToken.objects.filter(token=refresh_token).exists():
            raise AuthenticationFailed("Refresh token has been blacklisted")

        try:
            payload = decode_token(refresh_token)
        except AuthenticationFailed as e:
            self._deactivate_sessions(refresh_token, device_info)
            raise AuthenticationFailed(str(e))
        except jwt.InvalidSignatureError: 
            raise serializers.ValidationError("Invalid Token")
        except jwt.ExpiredSignatureError: 
            raise AuthenticationFailed('Refresh token expired')

        if not payload or payload.get("type") != "refresh":
            raise serializers.ValidationError("Invalid token type. Expected refresh token.")

        try:
            user = User.objects.get(id=payload["user_id"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        return {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
            "device_info": device_info,
            "ip_address": ip_address
        }

    def save(self, **kwargs):
        user = self.validated_data["user"]
        refresh_token = self.validated_data["refresh_token"]
        access_token = self.validated_data["access_token"]
        device_info = self.validated_data["device_info"]
        ip_address = self.validated_data["ip_address"]

        # Blacklist old tokens
        self._blacklist_token(refresh_token, user, "refresh")
        if access_token:
            try:
                access_payload = decode_token(access_token) 
                self._blacklist_token(access_token, user, "access")
            except AuthenticationFailed:
                pass

        # Generate new tokens
        new_access, new_refresh = generate_tokens(user)

        # Update or create session
        UserSession.objects.update_or_create(
            user=user,
            refresh_token=refresh_token,
            device_info=device_info,
            is_active=True,
            defaults={
                'session_token': new_access,
                'refresh_token': new_refresh,
                'ip_address': ip_address,
                'login_at': timezone.now(),
                'last_activity': timezone.now()
            }
        )

        return {
            "access": new_access,
            "refresh": new_refresh
        }

    def _blacklist_token(self, token, user_id, token_type):
        BlacklistedToken.objects.get_or_create(
            token=token,
            user=user_id,
            token_type=token_type
        )

    def _deactivate_sessions(self, token, device_info):
        try:
            payload = decode_token(token, allow_expired=True)
            user_id = payload.get("user_id")
            if user_id:
                UserSession.objects.filter(
                    user=user_id,
                    device_info=device_info,
                    is_active=True
                ).update(is_active=False, logout_at=timezone.now())
        except Exception as ex:
            logger.warning(f"Failed fallback decode for expired token: {str(ex)}")
