from django.db import models


class Training(models.Model):

    STATUS_CHOICES = (

        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Missed', 'Missed'),

    )

    session_title = models.CharField(
        max_length=200
    )

    trainer_name = models.CharField(
        max_length=200
    )

    training_date = models.DateField()

    duration_hours = models.PositiveIntegerField()

    training_type = models.CharField(
        max_length=100
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Scheduled'
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.session_title