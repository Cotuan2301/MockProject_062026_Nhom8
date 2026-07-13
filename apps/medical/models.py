"""
apps/medical/models.py
SC-022 Initial Assessment - Models
"""
from django.db import models
from django.conf import settings


class Assessment(models.Model):
    ASSESSMENT_TYPE_CHOICES = [
        ('initial', 'Initial Assessment'),
        ('periodic', 'Periodic Assessment'),
        ('quarterly', 'Quarterly Assessment'),
        ('annual', 'Annual Assessment'),
        ('change_of_condition', 'Change of Condition'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
    ]

    COGNITIVE_STATUS_CHOICES = [
        ('alert_oriented', 'Alert & Oriented'),
        ('alert_oriented_x1', 'Alert & Oriented x1'),
        ('alert_oriented_x2', 'Alert & Oriented x2'),
        ('alert_oriented_x3', 'Alert & Oriented x3'),
        ('confused', 'Confused'),
        ('lethargic', 'Lethargic'),
        ('obtunded', 'Obtunded'),
        ('stupor', 'Stupor'),
        ('coma', 'Coma'),
    ]

    CARE_LEVEL_CHOICES = [
        ('independent', 'Independent'),
        ('minimal_assist', 'Minimal Assist'),
        ('moderate_assist', 'Moderate Assist'),
        ('maximum_assist', 'Maximum Assist'),
        ('total_care', 'Total Care'),
    ]

    resident = models.ForeignKey(
        'residents.Resident',
        on_delete=models.CASCADE,
        related_name='assessments',
        verbose_name='Resident',
    )
    assessed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assessments_performed',
        verbose_name='Assessed By',
    )
    assessment_type = models.CharField(
        max_length=30, choices=ASSESSMENT_TYPE_CHOICES, default='initial',
    )
    assessment_date = models.DateTimeField(verbose_name='Assessment Date')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='draft',
    )
    cognitive_status = models.CharField(
        max_length=30, choices=COGNITIVE_STATUS_CHOICES, blank=True, default='',
    )
    care_level = models.CharField(
        max_length=20, choices=CARE_LEVEL_CHOICES, blank=True, default='',
    )
    allergies = models.TextField(blank=True, default='')
    clinical_notes = models.TextField(blank=True, default='')
    total_adl_score = models.IntegerField(default=0)
    max_adl_score = models.IntegerField(default=32)
    total_iadl_score = models.IntegerField(default=0)
    max_iadl_score = models.IntegerField(default=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assessments'
        ordering = ['-assessment_date']
        verbose_name = 'Assessment'
        verbose_name_plural = 'Assessments'

    def __str__(self):
        return f"{self.get_assessment_type_display()} - {self.resident.full_name} - {self.assessment_date.strftime('%Y-%m-%d')}"

    def recalculate_scores(self):
        adl_items = self.details.filter(category='adl')
        self.total_adl_score = sum(item.score or 0 for item in adl_items)
        self.max_adl_score = sum(item.max_score or 0 for item in adl_items)
        iadl_items = self.details.filter(category='iadl')
        self.total_iadl_score = sum(item.score or 0 for item in iadl_items)
        self.max_iadl_score = sum(item.max_score or 0 for item in iadl_items)
        if self.max_adl_score > 0:
            ratio = self.total_adl_score / self.max_adl_score
            if ratio >= 0.9:
                self.care_level = 'independent'
            elif ratio >= 0.7:
                self.care_level = 'minimal_assist'
            elif ratio >= 0.5:
                self.care_level = 'moderate_assist'
            elif ratio >= 0.25:
                self.care_level = 'maximum_assist'
            else:
                self.care_level = 'total_care'
        self.save(update_fields=[
            'total_adl_score', 'max_adl_score',
            'total_iadl_score', 'max_iadl_score',
            'care_level', 'updated_at',
        ])


class AssessmentDetail(models.Model):
    CATEGORY_CHOICES = [
        ('adl', 'Activities of Daily Living'),
        ('iadl', 'Instrumental ADL'),
        ('vital_sign', 'Vital Sign'),
    ]
    ADL_ITEMS = [
        ('bed_mobility', 'Bed Mobility'),
        ('transfer', 'Transfer'),
        ('locomotion', 'Locomotion'),
        ('dressing', 'Dressing'),
        ('eating', 'Eating'),
        ('toilet_use', 'Toilet Use'),
        ('personal_hygiene', 'Personal Hygiene'),
        ('bathing', 'Bathing'),
    ]
    IADL_ITEMS = [
        ('phone', 'Phone Use'),
        ('shopping', 'Shopping'),
        ('food_prep', 'Food Preparation'),
        ('housekeeping', 'Housekeeping'),
        ('laundry', 'Laundry'),
        ('transportation', 'Transportation'),
        ('medications', 'Medications'),
        ('finances', 'Finances'),
    ]
    VITAL_SIGN_ITEMS = [
        ('bp_systolic', 'BP Systolic', 'mmHg'),
        ('bp_diastolic', 'BP Diastolic', 'mmHg'),
        ('heart_rate', 'Heart Rate', 'bpm'),
        ('respiratory_rate', 'Respiratory Rate', 'breaths/min'),
        ('temperature', 'Temperature', '°F'),
        ('o2_saturation', 'O2 Saturation', '%'),
        ('weight', 'Weight', 'lbs'),
        ('height', 'Height', 'in'),
        ('bmi', 'BMI', 'kg/m²'),
    ]

    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name='details',
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    item_key = models.CharField(max_length=30)
    item_name = models.CharField(max_length=50)
    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField(null=True, blank=True)
    value = models.CharField(max_length=50, null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True)
    notes = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'assessment_details'
        unique_together = ['assessment', 'category', 'item_key']
        verbose_name = 'Assessment Detail'
        verbose_name_plural = 'Assessment Details'

    def __str__(self):
        display = self.score if self.score is not None else self.value
        return f"{self.assessment.id} - {self.item_name}: {display}"


class AssessmentDiagnosis(models.Model):
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name='diagnoses',
    )
    diagnosis_name = models.CharField(max_length=255)
    diagnosis_code = models.CharField(max_length=20, null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'assessment_diagnoses'
        ordering = ['-is_primary', 'diagnosis_name']
        verbose_name = 'Assessment Diagnosis'
        verbose_name_plural = 'Assessment Diagnoses'

    def __str__(self):
        code = f" ({self.diagnosis_code})" if self.diagnosis_code else ""
        return f"{self.diagnosis_name}{code}"


class CareLevel(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    min_adl_ratio = models.FloatField(null=True, blank=True)
    max_adl_ratio = models.FloatField(null=True, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'care_levels'
        ordering = ['sort_order']
        verbose_name = 'Care Level'
        verbose_name_plural = 'Care Levels'

    def __str__(self):
        return self.name