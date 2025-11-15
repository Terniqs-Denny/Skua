
from rest_framework import serializers

# from globals.models import Country, State
from users.models import User, UserProfile

class ShowUserValidateSerializer(serializers.Serializer):

    def validate(self, data):
        request = self.context.get("request")
        user_id = request.user.id

        try:
            user_obj = User.objects.get(id=user_id)
            data["user_id"] = user_obj
            data["user_profile"] = UserProfile.objects.get(user=user_obj.id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        return super().validate(data)

    
class StateMiniSerializer(serializers.ModelSerializer):

    class Meta:
        pass
        # model = State
        # fields = ["id", "name"]


class CountryMiniSerializer(serializers.ModelSerializer):

    class Meta:
        pass
        # model = Country
        # fields = ["id", "name"]


class UserProfileSerializer(serializers.ModelSerializer):
    state = StateMiniSerializer()
    country = StateMiniSerializer()
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        exclude = ["created_at", "updated_at"]

    def get_profile_pic(self, obj):
        pass
        # profile_picture = UserProfile.objects.get(id=obj.id).profile_pic if UserProfile.objects.get(id=obj.id) else None
        # profile_picture_link = ProfileStorageService().get_profile_picture(profile_picture, obj.user) if profile_picture else None
        # return profile_picture_link if profile_picture_link else None

class ShowUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    phone_number = serializers.IntegerField()
    user_profile = serializers.SerializerMethodField()


    def get_user_profile(self, obj):
        user_profile = UserProfile.objects.get(user=obj.id)
        return UserProfileSerializer(user_profile).data