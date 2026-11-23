from django.db import models


class CheckinSLA(models.Model):
    airline = models.CharField(max_length=20)
    aircraft_type = models.CharField(max_length=30)
    minimum_agents = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['airline', 'aircraft_type'],
                name='unique_checkin_sla_airline_aircraft',
            )
        ]
        ordering = ['airline', 'aircraft_type']

    def __str__(self):
        return f'{self.airline} / {self.aircraft_type}: {self.minimum_agents}'
