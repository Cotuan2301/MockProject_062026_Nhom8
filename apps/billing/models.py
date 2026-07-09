from django.db import models

class InsuranceProvider(models.Model):
    class ProviderType(models.TextChoices):
        MEDICARE = 'MEDICARE', 'Medicare'
        MEDICAID = 'MEDICAID', 'Medicaid'
        PRIVATE = 'PRIVATE', 'Private'
        OTHER = 'OTHER', 'Other'

    provider_name = models.CharField(max_length=200)
    provider_type = models.CharField(max_length=20, choices=ProviderType.choices)

    class Meta:
        db_table = 'insurance_providers'

class ResidentInsurancePolicy(models.Model):
    resident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE)
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE)
    policy_number_encrypted = models.CharField(max_length=512)
    group_number = models.CharField(max_length=100, null=True, blank=True)
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resident_insurance_policies'

class Invoice(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SENT = 'SENT', 'Sent'
        PARTIALLY_PAID = 'PARTIALLY_PAID', 'Partially Paid'
        PAID = 'PAID', 'Paid'
        OVERDUE = 'OVERDUE', 'Overdue'
        VOID = 'VOID', 'Void'

    resident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE)
    billing_period_start = models.DateField()
    billing_period_end = models.DateField()
    total_amount = models.DecimalField(max_digits=18, decimal_places=2)
    medicare_covered_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    medicaid_covered_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    private_insurance_covered_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    patient_responsibility_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    due_date = models.DateField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'invoices'

class InvoiceLineItem(models.Model):
    class ItemType(models.TextChoices):
        ROOM_BOARD = 'ROOM_BOARD', 'Room & Board'
        CARE_LEVEL = 'CARE_LEVEL', 'Care Level'
        MEDICATION = 'MEDICATION', 'Medication'
        THERAPY = 'THERAPY', 'Therapy'
        OTHER = 'OTHER', 'Other'

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    item_type = models.CharField(max_length=30, choices=ItemType.choices)
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'invoice_line_items'

class Payment(models.Model):
    class PayerType(models.TextChoices):
        MEDICARE = 'MEDICARE', 'Medicare'
        MEDICAID = 'MEDICAID', 'Medicaid'
        PRIVATE_INSURANCE = 'PRIVATE_INSURANCE', 'Private Insurance'
        FAMILY = 'FAMILY', 'Family'

    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'CREDIT_CARD', 'Credit Card'
        ACH = 'ACH', 'ACH'
        CHECK = 'CHECK', 'Check'
        CASH = 'CASH', 'Cash'
        INSURANCE_DIRECT = 'INSURANCE_DIRECT', 'Insurance Direct'

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payer_type = models.CharField(max_length=20, choices=PayerType.choices)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    payment_token_encrypted = models.CharField(max_length=512, null=True, blank=True)
    received_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'
