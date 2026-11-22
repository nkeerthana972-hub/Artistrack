from django.db import models

from artists.models import Artist


class Performance(models.Model):

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE
    )

    event_name = models.CharField(
        max_length=200
    )

    performance_date = models.DateField()

    score = models.IntegerField()

    feedback = models.TextField()

    coach_comments = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.artist} - {self.event_name}"