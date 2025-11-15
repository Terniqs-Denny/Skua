# userauth/models/blacklisted_token.py

from django.db import models
from users.models import User

class BlacklistedToken(models.Model):
    TOKEN_TYPE_CHOICES = [
        ('access', 'Access Token'),
        ('refresh', 'Refresh Token'),
    ]
    token = models.TextField(unique=True)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    token_type = models.CharField(max_length=10, choices=TOKEN_TYPE_CHOICES)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.token_type.capitalize()} token for user {self.user_id}"

    class Meta:
        db_table = "tblTokenBlacklisted"