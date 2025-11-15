
from rest_framework import serializers

# from globals.models import Country, State
from users.models import User, UserProfile
# from users.utils import ProfileStorageService

class UpdateUserSerializer(serializers.Serializer):
    # first_name = serializers.CharField(allow_null=True, required=False)
    # middle_name = serializers.CharField(allow_null=True, required=False)
    # last_name = serializers.CharField(allow_null=True, required=False)
    # email = serializers.CharField(allow_null=True, required=False)
    # phone_number = serializers.CharField(allow_null=True, required=False)
    address1 = serializers.CharField(allow_null=True, required=False)
    address2 = serializers.CharField(allow_null=True, required=False)
    # city = serializers.CharField(allow_null=True, required=False)
    # state = serializers.IntegerField(allow_null=True, required=False)
    country = serializers.IntegerField(allow_null=True, required=False)
    zip_code = serializers.CharField(allow_null=True, required=False)
    profile_pic = serializers.FileField(allow_null=True, required=False)


    def validate(self, data):
        request = self.context.get("request")
        user_id = request.user.id

        try:
            user_obj = User.objects.get(id=user_id)
            data["user_id"] = user_obj
            data["user_profile"] = UserProfile.objects.get(user=user_obj.id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        
        if "country" in data:
            pass
            # if "state" not in data or data["state"] == "":
            #     raise serializers.ValidationError("Updating the 'country' field also requires updating the 'state' field.")
            # try:
            #     country = Country.objects.get(id=data["country"])
            #     data["country"] = country
            # except Country.DoesNotExist:
            #     raise serializers.ValidationError("Country not found.")
            
        if "state" in data:
            pass

            # if "country" not in data:
            #     raise serializers.ValidationError("To update 'state', 'country' is required.")
            
            # try:
            #     data["state"] = State.objects.get(id=data["state"])
            # except State.DoesNotExist:
            #     raise serializers.ValidationError("State not found.")
            
            # state_exist = State.objects.filter(id=data["state"].id, country=data["country"]).exists()
            # if state_exist == False:
            #     raise serializers.ValidationError(f"'{data['state']}' is not part of the country '{data['country']}'")
        
        return super().validate(data)
    
    def update(self, validated_data):
        user = validated_data["user_id"]
        user_profile = validated_data["user_profile"]
        profile_pic = validated_data.pop("profile_pic", None)

        user_profile_fields = ["address1", "address2", "city", "state", "country", "zip_code"]

        if any(field in validated_data for field in user_profile_fields):
            for field in user_profile_fields:
                if field in validated_data:
                    setattr(user_profile, field, validated_data[field])
            user_profile.save()
        
        if profile_pic:
            pass
            # current_profile_pic = user_profile.profile_pic if user_profile else None
            # profile_storage_service = ProfileStorageService()
            
            # if current_profile_pic:
            #     profile_storage_service.delete_profile_picture(current_profile_pic, user)
            
            # profile_storage_service.upload_profile_picture(profile_pic, user)

            # user_profile.profile_pic = str(profile_pic)
            # user_profile.save()

        return user