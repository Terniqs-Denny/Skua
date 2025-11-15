# users/serializers/createuser_serializer.py

from rest_framework import serializers
from users.models import User, UserProfile

class UserCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email_id = serializers.EmailField()
    confirm_email = serializers.EmailField()
    mobile_number = serializers.CharField()

    def validate(self, data):

        if data["email_id"] != data["confirm_email"]:
            raise serializers.ValidationError("Email and confirm email must match.")

        if User.objects.filter(email=data["email_id"]).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        if User.objects.filter(phone_number=data["mobile_number"]).exists():
            raise serializers.ValidationError("A user with this mobile number already exists.")

        return data

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email_id"],
            phone_number=validated_data["mobile_number"]
        )

        UserProfile.objects.create(
            user=user,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )

        return user
