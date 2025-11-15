# userauth/serializers/requestotp_serializer.py

import random
from datetime import datetime
from rest_framework import serializers
from django.utils import timezone
from django.template.loader import render_to_string
from datetime import timedelta

# from globals.services.email_services.sendgrid_service import SendGridService
from users.models import User, UserProfile
from userauth.models import OTP

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile_number = serializers.CharField(required=False)
    purpose = serializers.CharField(default='login')  # Optional, can default to 'login'

    def validate(self, data):
        email = data.get('email')
        mobile = data.get('mobile_number')

        if bool(email) == bool(mobile):  # both or neither
            raise serializers.ValidationError("Provide either email or mobile_number, not both.")

        try:
            if email:
                user = User.objects.get(email=email)
                user_prof = UserProfile.objects.get(user=user.id)
                data['channel'] = 'email'
            else:
                user = User.objects.get(phone_number=mobile)
                user_prof = UserProfile.objects.get(user=user.id)
                data['channel'] = 'sms'

            data['user'] = user
            data["user_profile"] = user_prof
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        return data

    def create(self, validated_data):
        user = validated_data['user']
        user_profile = validated_data['user_profile']
        channel = validated_data['channel']
        purpose = validated_data['purpose']

        code = f"{random.randint(100000, 999999)}"
        # code = "123456"
        expires_at = timezone.now() + timedelta(minutes=5)

        otp = OTP.objects.create(
            user=user,
            code=code,
            expires_at=expires_at,
            channel=channel,
            purpose=purpose
        )

        if validated_data["channel"] == "email":

            template_variables = {
                "user_name": user_profile.first_name,
                "otp": code,
                "copyright_year": datetime.now().year
            }

            # email_subject = f"Email verification ({code}) for ({user_profile.first_name} {user_profile.last_name})"
            # rendered = render_to_string("email_templates/login_otp_template.html", template_variables)
            # SendGridService().send_mail(recipent_mails=[user.email], subject=email_subject, html_content=rendered)

        # You can return the OTP or just relevant info
        return {
            "user_id": str(user.id),
            "channel": channel,
            "code": code,
            "expires_at": expires_at
        }
