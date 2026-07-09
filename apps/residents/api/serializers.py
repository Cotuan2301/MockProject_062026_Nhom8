from rest_framework import serializers
from apps.residents.models import Resident, Address, ResidentSensitiveInfo, Contact, ResidentContact
from apps.rooms.models import Bed, Room
from apps.billing.models import InsuranceProvider, ResidentInsurancePolicy
from apps.medical.models import CareLevel, ResidentCareLevelHistory

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
        fields = ['first_name', 'last_name', 'phone_primary']

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
        fields = ['insurance_provider', 'policy_number_encrypted', 'effective_from', 'effective_to']

class CareLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareLevel
        fields = ['level_name']

class CareLevelHistorySerializer(serializers.ModelSerializer):
    care_level = CareLevelSerializer(read_only=True)
    class Meta:
        model = ResidentCareLevelHistory
        fields = ['care_level']


class ResidentDetailSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    confidential_data = serializers.SerializerMethodField()
    bed = BedSerializer(read_only=True)
    contacts = serializers.SerializerMethodField()
    insurances = serializers.SerializerMethodField()
    care_level_history = serializers.SerializerMethodField()

    class Meta:
        model = Resident
        fields = [
            'id', 'first_name', 'middle_name', 'last_name', 
            'date_of_birth', 'gender', 'marital_status', 'status',
            'confidential_data', 'address', 'bed', 
            'contacts', 'insurances', 'care_level_history'
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