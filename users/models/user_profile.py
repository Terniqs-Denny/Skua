# users/models/user_profile.py

from django.db import models
from users.models import User
# from globals.models.state import State
# from globals.models.country import Country

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    # state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    # country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "tblUserProfile"