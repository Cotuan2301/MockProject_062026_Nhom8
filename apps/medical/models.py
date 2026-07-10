from django.db import models

class CareLevel(models.Model):
    class LevelCode(models.TextChoices):
        INDEPENDENT_LIVING = 'INDEPENDENT_LIVING', 'Independent Living'
        ASSISTED_LIVING = 'ASSISTED_LIVING', 'Assisted Living'
        MEMORY_CARE = 'MEMORY_CARE', 'Memory Care'
        SKILLED_NURSING = 'SKILLED_NURSING', 'Skilled Nursing'
        HOSPICE = 'HOSPICE', 'Hospice'

    level_code = models.CharField(max_length=30, unique=True, choices=LevelCode.choices)
    level_name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'care_levels'

class CareLevelRate(models.Model):
    care_level = models.ForeignKey(CareLevel, on_delete=models.CASCADE)
    facility = models.ForeignKey('rooms.Facility', on_delete=models.CASCADE)
    daily_rate = models.DecimalField(max_digits=18, decimal_places=2)
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'care_level_rates'

class ResidentCareLevelHistory(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    resident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE)
    care_level = models.ForeignKey(CareLevel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'resident_care_level_history'

class PreAdmissionScreening(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        COMPLETED = 'COMPLETED', 'Completed'
        REJECTED = 'REJECTED', 'Rejected'

    status = models.CharField(max_length=20, choices=Status.choices)
    resident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE)
    screened_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, db_column='screened_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pre_admission_screenings'

class ClinicalRecord(models.Model):
    class RecordType(models.TextChoices):
        PROGRESS_NOTE = 'PROGRESS_NOTE', 'Progress Note'
        DIAGNOSIS = 'DIAGNOSIS', 'Diagnosis'
        LAB_RESULT = 'LAB_RESULT', 'Lab Result'
        ALLERGY = 'ALLERGY', 'Allergy'

    record_type = models.CharField(max_length=50, choices=RecordType.choices)
    description = models.TextField()
    resident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE)
    recorded_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, db_column='recorded_by')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clinical_records'

class Assessment(models.Model):
    adl_total_score = models.IntegerField()
    is_overridden = models.BooleanField(default=False)
    suggested_care_level = models.ForeignKey(CareLevel, on_delete=models.PROTECT, related_name='+')
    confirmed_care_level = models.ForeignKey(CareLevel, on_delete=models.PROTECT, related_name='+')
    resident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE)
    assessed_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, db_column='assessed_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'assessments'

class AssessmentMetric(models.Model):
    class Category(models.TextChoices):
        ADL = 'ADL', 'ADL'
        IADL = 'IADL', 'IADL'
        BRADEN = 'BRADEN', 'Braden'
        MORSE = 'MORSE', 'Morse'

    category = models.CharField(max_length=50, choices=Category.choices)
    metric_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'assessment_metrics'

class AssessmentDetail(models.Model):
    score = models.IntegerField()
    notes = models.CharField(max_length=500, null=True, blank=True)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    metric = models.ForeignKey(AssessmentMetric, on_delete=models.PROTECT)

    class Meta:
        db_table = 'assessment_details'

class VitalSign(models.Model):
    resident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE)
    recorded_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, db_column='recorded_by')
    blood_pressure_systolic = models.SmallIntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.SmallIntegerField(null=True, blank=True)
    heart_rate_bpm = models.SmallIntegerField(null=True, blank=True)
    respiratory_rate = models.SmallIntegerField(null=True, blank=True)
    temperature_fahrenheit = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    spo2_percentage = models.PositiveSmallIntegerField(null=True, blank=True)
    pain_scale = models.PositiveSmallIntegerField(null=True, blank=True)
    notes = models.CharField(max_length=500, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vital_signs'

class CarePlan(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        ACTIVE = 'ACTIVE', 'Active'
        RESOLVED = 'RESOLVED', 'Resolved'
        DISCONTINUED = 'DISCONTINUED', 'Discontinued'

    status = models.CharField(max_length=20, choices=Status.choices)
    significant_change_flag = models.BooleanField(default=False)
    resident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'care_plans'

class CareGoal(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        ACHIEVED = 'ACHIEVED', 'Achieved'
        NOT_MET = 'NOT_MET', 'Not Met'

    status = models.CharField(max_length=20, choices=Status.choices)
    care_plan = models.ForeignKey(CarePlan, on_delete=models.CASCADE)

    class Meta:
        db_table = 'care_goals'

class CareIntervention(models.Model):
    assigned_role = models.CharField(max_length=50)
    care_plan = models.ForeignKey(CarePlan, on_delete=models.CASCADE)

    class Meta:
        db_table = 'care_interventions'

class CareTask(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        MISSED = 'MISSED', 'Missed'

    task_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    is_abnormal_flagged = models.BooleanField(default=False)
    care_intervention = models.ForeignKey(CareIntervention, on_delete=models.CASCADE)
    assigned_cna = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_time = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'care_tasks'

class MedicationOrder(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        DISCONTINUED = 'DISCONTINUED', 'Discontinued'
        ON_HOLD = 'ON_HOLD', 'On Hold'

    drug_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    route = models.CharField(max_length=30)
    frequency = models.CharField(max_length=100)
    is_controlled_substance = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices)
    resident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE)
    prescribed_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, db_column='prescribed_by')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'medication_orders'

class MedicationSchedule(models.Model):
    order = models.ForeignKey(MedicationOrder, on_delete=models.CASCADE)
    scheduled_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'medication_schedules'

class MedicationLog(models.Model):
    class Status(models.TextChoices):
        ADMINISTERED = 'ADMINISTERED', 'Administered'
        REFUSED = 'REFUSED', 'Refused'
        HELD = 'HELD', 'Held'
        NOT_AVAILABLE = 'NOT_AVAILABLE', 'Not Available'

    status = models.CharField(max_length=20, choices=Status.choices)
    is_clinically_justified = models.BooleanField(default=False)
    override_reason = models.CharField(max_length=500, null=True, blank=True)
    order = models.ForeignKey(MedicationOrder, on_delete=models.CASCADE)
    administered_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='administered_meds', db_column='administered_by')
    witnessed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='witnessed_meds', db_column='witnessed_by')
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'medication_logs'

class IncidentSeverity(models.Model):
    level_name = models.CharField(max_length=50)
    chart_lock_trigger = models.BooleanField(default=False)

    class Meta:
        db_table = 'incident_severities'

class SlaConfig(models.Model):
    sla_window_hrs = models.IntegerField()
    severity = models.ForeignKey(IncidentSeverity, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sla_configs'

class Incident(models.Model):
    class IncidentType(models.TextChoices):
        FALL = 'FALL', 'Fall'
        MEDICATION_ERROR = 'MEDICATION_ERROR', 'Medication Error'
        ALTERCATION = 'ALTERCATION', 'Altercation'
        SKIN_TEAR = 'SKIN_TEAR', 'Skin Tear'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        UNDER_INVESTIGATION = 'UNDER_INVESTIGATION', 'Under Investigation'
        CLOSED = 'CLOSED', 'Closed'

    incident_type = models.CharField(max_length=50, choices=IncidentType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    description = models.TextField(null=True, blank=True)
    sla_deadline = models.DateTimeField()
    resident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE)
    severity = models.ForeignKey(IncidentSeverity, on_delete=models.PROTECT)
    reported_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, db_column='reported_by')
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'incidents'

class IncidentTimeline(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    action = models.TextField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    actor = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'incident_timelines'

class ChartLockEvent(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    unlocked_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, db_column='unlocked_by', null=True, blank=True)
    locked_by_system = models.BooleanField(default=True)
    unlock_reason = models.TextField(null=True, blank=True)
    event_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chart_lock_events'
