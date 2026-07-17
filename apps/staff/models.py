from django.db import models

class StaffingConfig(models.Model):
    min_hrs_per_resident_day = models.DecimalField(max_digits=5, decimal_places=2)
    warn_below_percentage = models.IntegerField()
    facility = models.ForeignKey('rooms.Facility', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'staffing_configs'

class Shift(models.Model):
    class ShiftName(models.TextChoices):
        DAY = 'DAY', 'Day'
        EVENING = 'EVENING', 'Evening'
        NIGHT = 'NIGHT', 'Night'

    facility = models.ForeignKey('rooms.Facility', on_delete=models.CASCADE)
    shift_name = models.CharField(max_length=20, choices=ShiftName.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'shifts'

class ShiftAssignment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CALLED_OUT = 'CALLED_OUT', 'Called Out'
        COMPLETED = 'COMPLETED', 'Completed'

    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    work_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    clock_in_at = models.DateTimeField(null=True, blank=True)
    clock_out_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'shift_assignments'