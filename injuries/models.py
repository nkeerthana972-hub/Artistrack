from django.db import models

from artists.models import Artist


class Injury(models.Model):

    STATUS_CHOICES = (

    ('open', 'Open'),

    ('recovering', 'Recovering'),

    ('resolved', 'Resolved'),
)
    
    SEVERITY_CHOICES = (

    ('low', 'Low'),

    ('medium', 'Medium'),

    ('high', 'High'),
)

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE
    )

    injury_name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    injury_date = models.DateField()

    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='open'
    )

    severity = models.CharField(
    max_length=20,
    choices=SEVERITY_CHOICES,
    default='low'
   )

    coach_notes = models.TextField(
        blank=True,
        null=True
    )

    medical_document = models.FileField(
    upload_to='injury_documents/',
    null=True,
    blank=True
    )

    resolved_date = models.DateField(
    null=True,
    blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.artist} - {self.injury_name}"