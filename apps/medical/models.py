from django.db import models
from django.contrib.auth.models import User
from apps.residents.models import Resident

class Assessment(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='assessments')
    version = models.IntegerField(default=1)
    assessment_type = models.CharField(max_length=50, default='initial')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_adl_score = models.IntegerField(default=0)
    
    adl_bed_mobility = models.IntegerField(default=0)
    adl_transfer = models.IntegerField(default=0)
    adl_locomotion = models.IntegerField(default=0)
    adl_dressing = models.IntegerField(default=0)
    adl_eating = models.IntegerField(default=0)
    adl_toilet_use = models.IntegerField(default=0)
    adl_personal_hygiene = models.IntegerField(default=0)
    adl_bathing = models.IntegerField(default=0)

    loc_tier = models.CharField(max_length=20, null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Assessment v{self.version} - {self.resident.full_name}"

class LOCClassification(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
    )

    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE, related_name='loc_classification')
    calculated_score = models.IntegerField()
    suggested_loc = models.CharField(max_length=50)
    final_loc = models.CharField(max_length=50, null=True, blank=True)
    is_overridden = models.BooleanField(default=False)
    override_reason = models.TextField(null=True, blank=True)
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"LOC for {self.assessment.resident.full_name} - {self.status}"

class LOCClassificationHistory(models.Model):
    loc_classification = models.ForeignKey(LOCClassification, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=50)
    action_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action_at = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return f"{self.action} on {self.action_at}"
