from rest_framework import serializers
from apps.medical.models import PreAdmissionScreening
from apps.residents.models import Admission, Resident
from apps.rooms.models import Bed

class PreAdmissionScreeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreAdmissionScreening
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'screened_by']

    def validate(self, data):
        # Validation for BR-06: Override reason required if flagged
        compliance_flagged = data.get('compliance_flagged', False)
        acuity_level = data.get('acuity_level')
        clinical_needs = data.get('clinical_needs', [])
        
        errors = {}
        if not acuity_level:
            errors['acuity_level'] = 'Acuity Level is required.'
        if not clinical_needs or len(clinical_needs) == 0:
            errors['clinical_needs'] = 'Please select at least one clinical need.'
            
        if errors:
            raise serializers.ValidationError(errors)
        
        # Auto flag if acuity is Moderate or High (simulated compliance check)
        if acuity_level in [PreAdmissionScreening.AcuityLevel.MODERATE, PreAdmissionScreening.AcuityLevel.HIGH]:
            compliance_flagged = True
            data['compliance_flagged'] = True
            
        if compliance_flagged:
            override_reason = data.get('override_reason')
            if not override_reason or len(override_reason.strip()) < 20:
                raise serializers.ValidationError({
                    'override_reason': 'Override reason is required and must be at least 20 characters when compliance check is flagged or acuity level is Moderate/High.'
                })
        
        return data

class AdmissionCreateSerializer(serializers.ModelSerializer):
    bed_id = serializers.IntegerField(write_only=True, required=True)
    
    # Extra fields for Care Team and Payer
    physician_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    physician_npi = serializers.CharField(write_only=True, required=False, allow_blank=True)
    nurse_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    payer_source = serializers.CharField(write_only=True, required=False, allow_blank=True)
    payer_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = Admission
        fields = [
            'resident', 'facility', 'admission_date', 
            'verification_method', 'consent_signature', 'consent_file',
            'bed_id', 'order_date',
            'physician_name', 'physician_npi', 'nurse_name',
            'payer_source', 'payer_name'
        ]

    from django.db import transaction
    @transaction.atomic
    def create(self, validated_data):
        from apps.accounts.models import User, Role
        from apps.billing.models import InsuranceProvider, ResidentInsurancePolicy
        
        bed_id = validated_data.pop('bed_id', None)
        physician_name = validated_data.pop('physician_name', None)
        physician_npi = validated_data.pop('physician_npi', None)
        nurse_name = validated_data.pop('nurse_name', None)
        payer_source = validated_data.pop('payer_source', None)
        payer_name = validated_data.pop('payer_name', None)
        
        # 1. Auto-provision Physician
        physician = None
        if physician_name:
            role_doctor, _ = Role.objects.get_or_create(role_name='Doctor')
            # Assuming format "Dr. Alan Cho, MD" - just use as last_name for simplicity in mock
            physician = User.objects.filter(last_name=physician_name, npi=physician_npi).first()
            if not physician:
                physician = User.objects.create(
                    employee_code=f"DOC_{physician_npi or 'TEMP'}",
                    email=f"doc_{physician_npi or 'temp'}@test.com",
                    password_hash='dummy',
                    first_name='',
                    last_name=physician_name,
                    npi=physician_npi,
                    role=role_doctor
                )
        
        # 2. Auto-provision Nurse
        nurse = None
        if nurse_name:
            role_nurse, _ = Role.objects.get_or_create(role_name='Nurse')
            nurse = User.objects.filter(last_name=nurse_name).first()
            if not nurse:
                nurse = User.objects.create(
                    employee_code=f"NUR_{nurse_name.replace(' ', '')}",
                    email=f"nur_{nurse_name.replace(' ', '')}@test.com",
                    password_hash='dummy',
                    first_name='',
                    last_name=nurse_name,
                    role=role_nurse
                )
                
        # 3. Auto-provision Insurance
        if payer_source or payer_name:
            provider, _ = InsuranceProvider.objects.get_or_create(
                provider_name=payer_name or payer_source,
                defaults={'provider_type': payer_source or 'OTHER'}
            )
            ResidentInsurancePolicy.objects.get_or_create(
                resident=validated_data['resident'],
                insurance_provider=provider,
                defaults={
                    'policy_number_encrypted': 'PENDING_AT_ADMISSION',
                    'effective_from': validated_data['admission_date']
                }
            )

        validated_data['admitting_physician'] = physician
        validated_data['admitting_nurse'] = nurse
        
        # Save Admission record
        admission = Admission.objects.create(**validated_data)
        
        # Update Bed Status
        bed = None
        if bed_id:
            bed = Bed.objects.get(pk=bed_id)
            bed.status = 'OCCUPIED'
            bed.save()
            
        # Update Resident Status & Bed
        resident = validated_data['resident']
        resident.status = Resident.Status.ACTIVE
        if bed:
            resident.bed = bed
        resident.save()
            
        return admission
