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