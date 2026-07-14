from rest_framework import serializers
from apps.residents.models import Resident, Address, ResidentSensitiveInfo, Contact, ResidentContact, Admission
from apps.rooms.models import Bed, Room
from apps.billing.models import InsuranceProvider, ResidentInsurancePolicy
from apps.medical.models import CareLevel, ResidentCareLevelHistory, ClinicalRecord, Assessment

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street_line1', 'city', 'state', 'address_type']

class ConfidentialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentSensitiveInfo
        fields = ['ssn_encrypted']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_number']

class BedSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    class Meta:
        model = Bed
        fields = ['bed_number', 'room']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_primary', 'phone_secondary']

class ResidentContactSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    class Meta:
        model = ResidentContact
        fields = ['contact', 'relationship_type', 'is_emergency_contact']

class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProvider
        fields = ['provider_name', 'provider_type']

class ResidentInsuranceSerializer(serializers.ModelSerializer):
    insurance_provider = InsuranceProviderSerializer(read_only=True)
    class Meta:
        model = ResidentInsurancePolicy
        fields = ['insurance_provider', 'policy_number_encrypted', 'group_number', 'effective_from', 'effective_to']

class CareLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareLevel
        fields = ['level_name']

class CareLevelHistorySerializer(serializers.ModelSerializer):
    care_level = CareLevelSerializer(read_only=True)
    class Meta:
        model = ResidentCareLevelHistory
        fields = ['care_level']

class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = ['admission_date', 'discharge_date', 'discharge_reason', 'referral_source']

class ClinicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalRecord
        fields = ['record_type', 'description', 'created_at']

class AssessmentSerializer(serializers.ModelSerializer):
    confirmed_care_level = CareLevelSerializer(read_only=True)
    class Meta:
        model = Assessment
        fields = ['adl_total_score', 'confirmed_care_level', 'created_at']


class ResidentDetailSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    confidential_data = serializers.SerializerMethodField()
    bed = BedSerializer(read_only=True)
    contacts = serializers.SerializerMethodField()
    insurances = serializers.SerializerMethodField()
    care_level_history = serializers.SerializerMethodField()
    admissions = serializers.SerializerMethodField()
    clinical_records = serializers.SerializerMethodField()
    assessments = serializers.SerializerMethodField()

    class Meta:
        model = Resident
        fields = [
            'id', 'first_name', 'middle_name', 'last_name', 
            'date_of_birth', 'gender', 'marital_status', 'status',
            'has_dnr', 'confidential_data', 'address', 'bed', 
            'contacts', 'insurances', 'care_level_history',
            'admissions', 'clinical_records', 'assessments'
        ]

    def get_confidential_data(self, obj):
        if hasattr(obj, 'residentsensitiveinfo'):
            return ConfidentialDataSerializer(obj.residentsensitiveinfo).data
        return None

    def get_contacts(self, obj):
        qs = obj.residentcontact_set.all()
        return ResidentContactSerializer(qs, many=True).data

    def get_insurances(self, obj):
        qs = obj.residentinsurancepolicy_set.all()
        return ResidentInsuranceSerializer(qs, many=True).data
        
    def get_care_level_history(self, obj):
        qs = obj.residentcarelevelhistory_set.all()
        return CareLevelHistorySerializer(qs, many=True).data

    def get_admissions(self, obj):
        qs = obj.admission_set.all()
        return AdmissionSerializer(qs, many=True).data

    def get_clinical_records(self, obj):
        qs = obj.clinicalrecord_set.all()
        return ClinicalRecordSerializer(qs, many=True).data

    def get_assessments(self, obj):
        qs = obj.assessment_set.all()
        return AssessmentSerializer(qs, many=True).data

class ResidentCreateUpdateSerializer(serializers.ModelSerializer):
    ssn = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    
    # Address
    address_line1 = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    address_line2 = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    address_city = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    address_state = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    address_zip_code = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    # Contact (Self)
    phone_primary = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    phone_secondary = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    # Emergency Contact
    emergency_first_name = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    emergency_last_name = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    emergency_phone_primary = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    emergency_phone_secondary = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    
    # POA Contact
    poa_first_name = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    poa_last_name = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    poa_phone_primary = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    poa_phone_secondary = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    poa_relationship = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    
    # Insurance / Payer
    insurance_provider_name = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    insurance_provider_type = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    policy_number = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    policy_effective_from = serializers.DateField(write_only=True, required=False, allow_null=True)
    policy_effective_to = serializers.DateField(write_only=True, required=False, allow_null=True)
    auth_number = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Resident
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth', 'gender', 
            'marital_status', 'status', 'has_dnr', 
            'ssn', 'referral_source', 'referral_facility', 'referred_by',
            'address_line1', 'address_line2', 'address_city', 'address_state', 'address_zip_code',
            'phone_primary', 'phone_secondary', 
            'emergency_first_name', 'emergency_last_name', 'emergency_phone_primary', 'emergency_phone_secondary',
            'poa_first_name', 'poa_last_name', 'poa_phone_primary', 'poa_phone_secondary', 'poa_relationship',
            'insurance_provider_name', 'insurance_provider_type', 'policy_number', 'policy_effective_from', 'policy_effective_to',
            'auth_number'
        ]

    def validate(self, data):
        # Validate required fields (Red * on screen)
        if not self.instance: # Only validate on Create
            required_custom_fields = {
                'ssn': 'SSN is required.',
                'referral_source': 'Referral Source is required.',
                'phone_primary': 'Primary Phone is required.',
                'emergency_first_name': 'Emergency Contact First Name is required.',
                'emergency_last_name': 'Emergency Contact Last Name is required.',
                'emergency_phone_primary': 'Emergency Contact Primary Phone is required.',
                'insurance_provider_name': 'Insurance Provider Name is required.'
            }
            errors = {}
            for field, msg in required_custom_fields.items():
                if not data.get(field) or str(data.get(field)).strip() == '':
                    errors[field] = msg
            if errors:
                raise serializers.ValidationError(errors)

        first_name = data.get('first_name', getattr(self.instance, 'first_name', None))
        last_name = data.get('last_name', getattr(self.instance, 'last_name', None))
        dob = data.get('date_of_birth', getattr(self.instance, 'date_of_birth', None))
        
        if first_name and last_name and dob:
            duplicates = Resident.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name,
                date_of_birth=dob
            )
            if self.instance:
                duplicates = duplicates.exclude(pk=self.instance.pk)
                
            if duplicates.exists():
                raise serializers.ValidationError({
                    "non_field_errors": ["Similar resident name exists. Please verify before saving."]
                })
                
        # SSN Validation (Format & Uniqueness)
        ssn = data.get('ssn', None)
        if ssn:
            import re
            # Check format (e.g.: 123-45-6789 or XXX-XX-6789)
            if not re.match(r'^[\dX]{3}-[\dX]{2}-[\dX]{4}$', ssn, re.IGNORECASE):
                raise serializers.ValidationError({
                    "ssn": "Invalid SSN format. Expected format: XXX-XX-XXXX."
                })
            
            # Check SSN duplicate
            ssn_duplicates = ResidentSensitiveInfo.objects.filter(ssn_encrypted=ssn)
            if self.instance:
                ssn_duplicates = ssn_duplicates.exclude(resident=self.instance)
                
            if ssn_duplicates.exists():
                raise serializers.ValidationError({
                    "ssn": "A resident with this SSN already exists."
                })
                
        # Policy Number Validation (Uniqueness)
        policy_number = data.get('policy_number', None)
        if policy_number:
            policy_duplicates = ResidentInsurancePolicy.objects.filter(policy_number_encrypted=policy_number)
            if self.instance:
                policy_duplicates = policy_duplicates.exclude(resident=self.instance)
                
            if policy_duplicates.exists():
                raise serializers.ValidationError({
                    "policy_number": "A resident with this Policy Number already exists."
                })
                
        return data

    from django.db import transaction
    @transaction.atomic
    def create(self, validated_data):
        from apps.rooms.models import Facility
        
        ssn = validated_data.pop('ssn', None)
        
        address_line1 = validated_data.pop('address_line1', None)
        address_line2 = validated_data.pop('address_line2', None)
        address_city = validated_data.pop('address_city', None)
        address_state = validated_data.pop('address_state', None)
        address_zip_code = validated_data.pop('address_zip_code', None)
        
        phone_primary = validated_data.pop('phone_primary', None)
        phone_secondary = validated_data.pop('phone_secondary', None)
        
        emergency_first_name = validated_data.pop('emergency_first_name', None)
        emergency_last_name = validated_data.pop('emergency_last_name', None)
        emergency_phone_primary = validated_data.pop('emergency_phone_primary', None)
        emergency_phone_secondary = validated_data.pop('emergency_phone_secondary', None)
        
        poa_first_name = validated_data.pop('poa_first_name', None)
        poa_last_name = validated_data.pop('poa_last_name', None)
        poa_phone_primary = validated_data.pop('poa_phone_primary', None)
        poa_phone_secondary = validated_data.pop('poa_phone_secondary', None)
        poa_relationship = validated_data.pop('poa_relationship', None)
        
        insurance_provider_name = validated_data.pop('insurance_provider_name', None)
        insurance_provider_type = validated_data.pop('insurance_provider_type', None)
        policy_number = validated_data.pop('policy_number', None)
        policy_effective_from = validated_data.pop('policy_effective_from', None)
        policy_effective_to = validated_data.pop('policy_effective_to', None)
        auth_number = validated_data.pop('auth_number', None)

        address_obj = None
        if address_line1 or address_city or address_state:
            address_obj = Address.objects.create(
                street_line1=address_line1 or '', 
                street_line2=address_line2 or '', 
                city=address_city or '', 
                state=address_state or '', 
                zip_code=address_zip_code or '', 
                address_type='HOME'
            )
            validated_data['address'] = address_obj
            
        resident = Resident.objects.create(**validated_data)
        
        if ssn:
            ResidentSensitiveInfo.objects.create(resident=resident, ssn_encrypted=ssn)
                
        if phone_primary or phone_secondary:
            c_self = Contact.objects.create(
                first_name=resident.first_name, 
                last_name=resident.last_name, 
                phone_primary=phone_primary or '',
                phone_secondary=phone_secondary or ''
            )
            ResidentContact.objects.create(resident=resident, contact=c_self, relationship_type='Self')
            
        if emergency_first_name or emergency_last_name:
            c_em = Contact.objects.create(
                first_name=emergency_first_name or '', 
                last_name=emergency_last_name or '', 
                phone_primary=emergency_phone_primary or '',
                phone_secondary=emergency_phone_secondary or ''
            )
            ResidentContact.objects.create(resident=resident, contact=c_em, relationship_type='Emergency', is_emergency_contact=True)
            
        if poa_first_name or poa_last_name:
            c_poa = Contact.objects.create(
                first_name=poa_first_name or '', 
                last_name=poa_last_name or '', 
                phone_primary=poa_phone_primary or '',
                phone_secondary=poa_phone_secondary or ''
            )
            ResidentContact.objects.create(resident=resident, contact=c_poa, relationship_type=poa_relationship or 'POA', is_guarantor=True)
            
        if insurance_provider_name or policy_number:
            provider = None
            if insurance_provider_name:
                provider, _ = InsuranceProvider.objects.get_or_create(provider_name=insurance_provider_name, defaults={'provider_type': insurance_provider_type or 'OTHER'})
            elif insurance_provider_type:
                provider = InsuranceProvider.objects.filter(provider_type=insurance_provider_type).first()
                
            if provider:
                ResidentInsurancePolicy.objects.create(
                    resident=resident,
                    insurance_provider=provider,
                    policy_number_encrypted=policy_number or '',
                    effective_from=policy_effective_from or resident.date_of_birth,
                    effective_to=policy_effective_to,
                    auth_number=auth_number
                )
        return resident

    from django.db import transaction
    @transaction.atomic
    def update(self, instance, validated_data):
        ssn = validated_data.pop('ssn', None)
        
        address_line1 = validated_data.pop('address_line1', None)
        address_line2 = validated_data.pop('address_line2', None)
        address_city = validated_data.pop('address_city', None)
        address_state = validated_data.pop('address_state', None)
        address_zip_code = validated_data.pop('address_zip_code', None)
        
        phone_primary = validated_data.pop('phone_primary', None)
        phone_secondary = validated_data.pop('phone_secondary', None)
        
        emergency_first_name = validated_data.pop('emergency_first_name', None)
        emergency_last_name = validated_data.pop('emergency_last_name', None)
        emergency_phone_primary = validated_data.pop('emergency_phone_primary', None)
        emergency_phone_secondary = validated_data.pop('emergency_phone_secondary', None)
        
        poa_first_name = validated_data.pop('poa_first_name', None)
        poa_last_name = validated_data.pop('poa_last_name', None)
        poa_phone_primary = validated_data.pop('poa_phone_primary', None)
        poa_phone_secondary = validated_data.pop('poa_phone_secondary', None)
        poa_relationship = validated_data.pop('poa_relationship', None)
        
        insurance_provider_name = validated_data.pop('insurance_provider_name', None)
        insurance_provider_type = validated_data.pop('insurance_provider_type', None)
        policy_number = validated_data.pop('policy_number', None)
        policy_effective_from = validated_data.pop('policy_effective_from', None)
        policy_effective_to = validated_data.pop('policy_effective_to', None)
        auth_number = validated_data.pop('auth_number', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if ssn:
            info, _ = ResidentSensitiveInfo.objects.get_or_create(resident=instance)
            info.ssn_encrypted = ssn
            info.save()
            
        if address_line1 is not None or address_city is not None or address_state is not None:
            if instance.address:
                if address_line1 is not None: instance.address.street_line1 = address_line1
                if address_line2 is not None: instance.address.street_line2 = address_line2
                if address_city is not None: instance.address.city = address_city
                if address_state is not None: instance.address.state = address_state
                if address_zip_code is not None: instance.address.zip_code = address_zip_code
                instance.address.save()
            else:
                addr = Address.objects.create(
                    street_line1=address_line1 or '', 
                    street_line2=address_line2 or '', 
                    city=address_city or '', 
                    state=address_state or '', 
                    zip_code=address_zip_code or '', 
                    address_type='HOME'
                )
                instance.address = addr
                instance.save()
                
        # Update self contact (Self)
        if phone_primary is not None or phone_secondary is not None:
            self_rc = instance.residentcontact_set.filter(relationship_type='Self').first()
            if self_rc:
                if phone_primary is not None:
                    self_rc.contact.phone_primary = phone_primary
                if phone_secondary is not None:
                    self_rc.contact.phone_secondary = phone_secondary
                self_rc.contact.save()
            else:
                c_self = Contact.objects.create(
                    first_name=instance.first_name, 
                    last_name=instance.last_name, 
                    phone_primary=phone_primary or '',
                    phone_secondary=phone_secondary or ''
                )
                ResidentContact.objects.create(resident=instance, contact=c_self, relationship_type='Self')
                
        # Update Emergency Contact
        if emergency_first_name is not None or emergency_last_name is not None or emergency_phone_primary is not None:
            em_rc = instance.residentcontact_set.filter(is_emergency_contact=True).first()
            if em_rc:
                if emergency_first_name is not None: em_rc.contact.first_name = emergency_first_name
                if emergency_last_name is not None: em_rc.contact.last_name = emergency_last_name
                if emergency_phone_primary is not None:
                    em_rc.contact.phone_primary = emergency_phone_primary
                if emergency_phone_secondary is not None:
                    em_rc.contact.phone_secondary = emergency_phone_secondary
                em_rc.contact.save()
            else:
                c_em = Contact.objects.create(
                    first_name=emergency_first_name or '', 
                    last_name=emergency_last_name or '', 
                    phone_primary=emergency_phone_primary or '',
                    phone_secondary=emergency_phone_secondary or ''
                )
                ResidentContact.objects.create(resident=instance, contact=c_em, relationship_type='Emergency', is_emergency_contact=True)
                
        # Update POA Contact
        if poa_first_name is not None or poa_last_name is not None or poa_phone_primary is not None:
            poa_rc = instance.residentcontact_set.filter(is_guarantor=True).first()
            if poa_rc:
                if poa_first_name is not None: poa_rc.contact.first_name = poa_first_name
                if poa_last_name is not None: poa_rc.contact.last_name = poa_last_name
                if poa_phone_primary is not None:
                    poa_rc.contact.phone_primary = poa_phone_primary
                if poa_phone_secondary is not None:
                    poa_rc.contact.phone_secondary = poa_phone_secondary
                poa_rc.contact.save()
                if poa_relationship is not None:
                    poa_rc.relationship_type = poa_relationship
                    poa_rc.save()
            elif poa_first_name or poa_last_name:
                c_poa = Contact.objects.create(
                    first_name=poa_first_name or '', 
                    last_name=poa_last_name or '', 
                    phone_primary=poa_phone_primary or '',
                    phone_secondary=poa_phone_secondary or ''
                )
                ResidentContact.objects.create(resident=instance, contact=c_poa, relationship_type=poa_relationship or 'POA', is_guarantor=True)
                
        # Update Payer / Insurance Policy
        if insurance_provider_name or policy_number or policy_effective_from or policy_effective_to:
            policy = instance.residentinsurancepolicy_set.first()
            provider = None
            if insurance_provider_name:
                provider, _ = InsuranceProvider.objects.get_or_create(provider_name=insurance_provider_name, defaults={'provider_type': insurance_provider_type or 'OTHER'})
            elif insurance_provider_type:
                provider = InsuranceProvider.objects.filter(provider_type=insurance_provider_type).first()
                
            if policy:
                if provider:
                    policy.insurance_provider = provider
                if policy_number is not None:
                    policy.policy_number_encrypted = policy_number
                if policy_effective_from is not None:
                    policy.effective_from = policy_effective_from
                if policy_effective_to is not None:
                    policy.effective_to = policy_effective_to
                policy.save()
            elif provider:
                ResidentInsurancePolicy.objects.create(
                    resident=instance,
                    insurance_provider=provider,
                    policy_number_encrypted=policy_number or '',
                    effective_from=policy_effective_from or instance.date_of_birth,
                    effective_to=policy_effective_to
                )
                
        return instance
