from django.db import models
from django.contrib.auth.models import User
from apps.residents.models import Resident

class ResidentCareLevelHistory(models.Model):
    class ActionChoices(models.TextChoices):
        CONFIRMED = 'Confirmed', 'Confirmed'
        OVERRIDDEN = 'Overridden', 'Overridden'

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='loc_history')
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=ActionChoices.choices)
    previous_tier = models.CharField(max_length=50, null=True, blank=True)
    new_tier = models.CharField(max_length=50)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='loc_actions')
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.resident.full_name} - {self.action} to {self.new_tier} on {self.date.strftime('%Y-%m-%d')}"
