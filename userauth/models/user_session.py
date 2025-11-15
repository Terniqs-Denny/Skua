# userauth/models/user_session.py

from django.db import models
from users.models import User

class UserSession(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=512)
    refresh_token = models.CharField(max_length=512)
    device_info = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    login_at = models.DateTimeField(auto_now_add=True)
    logout_at = models.DateTimeField(blank=True, null=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "tblUserSession"