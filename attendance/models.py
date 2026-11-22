from django.db import models

from artists.models import Artist
from trainings.models import Training

class Attendance(models.Model):

    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE
    )

    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        null=True,
        blank=True
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    marked_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.artist} - {self.date}"