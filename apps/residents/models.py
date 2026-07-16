from django.db import models


class Resident(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        DISCHARGED = 'discharged', 'Discharged'
        PENDING = 'pending', 'Pending'

    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        OTHER = 'other', 'Other'

    class LocTier(models.TextChoices):
        TIER_1 = 'Tier 1', 'Tier 1'
        TIER_2 = 'Tier 2', 'Tier 2'
        TIER_3 = 'Tier 3', 'Tier 3'
        TIER_4 = 'Tier 4', 'Tier 4'

    resident_id = models.CharField(max_length=20, unique=True, verbose_name='Resident ID')
    full_name = models.CharField(max_length=150)
    room_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.OTHER)
    payer_source = models.CharField(max_length=50)
    admission_date = models.DateField()
    loc_tier = models.CharField(max_length=10, choices=LocTier.choices, default=LocTier.TIER_1)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f'{self.resident_id} - {self.full_name}'

    @property
    def year_of_birth(self):
        return self.date_of_birth.year if self.date_of_birth else None
