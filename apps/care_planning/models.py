from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CarePlan(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING_REVIEW = 'pending_review', 'Pending Review'
        ACTIVE = 'active', 'Active'
        REVIEW_DUE = 'review_due', 'Review Due'
        NEEDS_UPDATE = 'needs_update', 'Needs Update'

    resident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE, related_name='care_plans')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    last_review_date = models.DateField(null=True, blank=True)
    next_review_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_care_plans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Care Plan for {self.resident.full_name} ({self.get_status_display()})"
