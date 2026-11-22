from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('director', 'Director'),
        ('coach', 'Coach'),
        ('artist', 'Artist'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
    
class AuditLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    action = models.CharField(max_length=255)

    details = models.TextField(blank=True, null=True)  

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"
    


class AdminOTP(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def is_expired(self):

        return timezone.now() > self.created_at + timedelta(minutes=5)
# Create your models here.
