# userauth/serializers/verifyotp_serializer.py

from rest_framework import serializers
from django.utils import timezone

from users.models import User
from userauth.models import OTP, UserSession
from userauth.utils.jwt_utils import generate_tokens


class VerifyOTPSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    otp = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(id=data['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        otp_obj = OTP.objects.filter(
            user=user,
            code=data['otp'],
            purpose="login",
            expires_at__gt=timezone.now(),
            is_verified=False
        ).order_by('-created_at').first()

        if not otp_obj:
            # Optionally increment failed attempt
            recent_otp = OTP.objects.filter(
                user=user,
                purpose="login"
            ).order_by('-created_at').first()

            if recent_otp:
                recent_otp.attempt_count += 1
                recent_otp.save(update_fields=['attempt_count'])

            raise serializers.ValidationError("Invalid or expired OTP.")

        self.user = user
        self.otp_obj = otp_obj
        return data

    def save(self, **kwargs):
        request = self.context['request']
        ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')
        device_info = request.META.get('HTTP_USER_AGENT', 'Unknown Device')

        # Mark OTP as verified
        self.otp_obj.is_verified = True
        self.otp_obj.save()

        # Generate JWT tokens
        access_token, refresh_token = generate_tokens(self.user)

        # Create session
        session = UserSession.objects.create(
            user=self.user,
            session_token=access_token,
            refresh_token=refresh_token,
            device_info=device_info,
            ip_address=ip_address,
            is_active=True,
            login_at=timezone.now(),
            last_activity=timezone.now()
        )

        return {
            "access": access_token,
            "refresh": refresh_token,
            "user_id": str(self.user.id),
            "session_id": session.id
        }
