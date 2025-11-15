# userauth/models/otp.py

from django.db import models
from users.models import User

class OTP(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempt_count = models.IntegerField(default=0)
    channel = models.CharField(max_length=20)  # e.g., 'email', 'sms'
    purpose = models.CharField(max_length=50)  # e.g., 'login', 'signup'

    class Meta:
        db_table = 'tblOTP'