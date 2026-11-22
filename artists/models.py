from django.db import models
from accounts.models import CustomUser


class Artist(models.Model):

    GENDER_CHOICES = (

        ('male', 'Male'),
        ('female', 'Female'),

    )

    user = models.OneToOneField(

        CustomUser,

        on_delete=models.CASCADE,

        null=True,
        blank=True

    )

    first_name = models.CharField(
        max_length=100,
        blank=True
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    gender = models.CharField(

        max_length=10,

        choices=GENDER_CHOICES,

        blank=True

    )

    dance_style = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    email = models.EmailField(
        unique=True
    )

    joined_date = models.DateField(
        auto_now_add=True
    )

    profile_image = models.ImageField(

        upload_to='artist_profiles/',

        null=True,
        blank=True

    )

    def __str__(self):

        if self.first_name:

            return f"{self.first_name} {self.last_name}"

        return self.user.username