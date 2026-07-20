from django.db import models


class CareLevel(models.Model):
    id = models.BigAutoField(primary_key=True)

    LEVEL_CHOICES = [
        ("INDEPENDENT_LIVING", "Independent Living"),
        ("ASSISTED_LIVING", "Assisted Living"),
        ("MEMORY_CARE", "Memory Care"),
        ("SKILLED_NURSING", "Skilled Nursing"),
        ("HOSPICE", "Hospice"),
    ]

    level_code = models.CharField(
        max_length=30,
        unique=True,
        choices=LEVEL_CHOICES
    )

    level_name = models.CharField(max_length=100)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "care_levels"

    def __str__(self):
        return self.level_name


class CarePlan(models.Model):
    id = models.BigAutoField(primary_key=True)

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("ACTIVE", "Active"),
        ("RESOLVED", "Resolved"),
        ("DISCONTINUED", "Discontinued"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT"
    )

    significant_change_flag = models.BooleanField(default=False)

    # Tạm thời để BigInteger, sau này có thể đổi sang ForeignKey Resident
    resident_id = models.BigIntegerField()

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "care_plans"

    def __str__(self):
        return f"Care Plan #{self.id}"


class CareGoal(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )

    STATUS_CHOICES = [
        ("IN_PROGRESS", "In Progress"),
        ("ACHIEVED", "Achieved"),
        ("NOT_MET", "Not Met"),
    ]

    care_plan = models.ForeignKey(
        CarePlan,
        on_delete=models.CASCADE,
        db_column="care_plan_id",
        related_name="goals"
    )

    goal = models.TextField(
        null=True,
        blank=True
    )

    measure = models.TextField(
        null=True,
        blank=True
    )

    task = models.TextField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="IN_PROGRESS"
    )

    is_deleted = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = "care_goals"

    def __str__(self):
        return f"Care Goal #{self.id}"


# ==========================================
# HOLIDAY MODEL (Ánh xạ bảng Holidays trên SQL Server)
# ==========================================
class Holiday(models.Model):
    holiday_id = models.AutoField(primary_key=True, db_column='HolidayID')
    holiday_date = models.DateField(unique=True, db_column='HolidayDate')
    holiday_name = models.CharField(max_length=250, db_column='HolidayName')
    is_national_holiday = models.BooleanField(default=True, db_column='IsNationalHoliday')
    description = models.CharField(max_length=500, blank=True, null=True, db_column='Description')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CreatedAt')

    class Meta:
        db_table = 'Holidays'  # Tên bảng trùng khớp 100% với SQL Server SSMS
        managed = False        # Đặt False để Django không tự ý tạo/thay đổi structure bảng SQL Server

    def __str__(self):
        return f"{self.holiday_name} ({self.holiday_date})"