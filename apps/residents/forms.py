from django import forms
from .models import Resident

class ResidentForm(forms.ModelForm):
    # Sensitive Info
    ssn = forms.CharField(required=False)
    
    # Address
    address_line1 = forms.CharField(required=False)
    address_line2 = forms.CharField(required=False)
    address_city = forms.CharField(required=False)
    address_state = forms.CharField(required=False)
    # address_zip_code = forms.CharField(required=False)

    # Contact (Self)
    phone_primary = forms.CharField(required=False)
    phone_secondary = forms.CharField(required=False)

    # Emergency Contact
    emergency_first_name = forms.CharField(required=False)
    emergency_last_name = forms.CharField(required=False)
    emergency_phone_primary = forms.CharField(required=False)
    emergency_phone_secondary = forms.CharField(required=False)
    
    # POA (Authorized Representative)
    poa_on_file = forms.BooleanField(required=False, initial=False)
    poa_first_name = forms.CharField(required=False)
    poa_last_name = forms.CharField(required=False)
    poa_phone_primary = forms.CharField(required=False)
    poa_phone_secondary = forms.CharField(required=False)
    poa_relationship = forms.CharField(required=False)
    
    # Insurance / Payer
    insurance_provider_name = forms.CharField(required=False)
    insurance_provider_type = forms.CharField(required=False)
    policy_number = forms.CharField(required=False)
    policy_effective_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    policy_effective_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    auth_number = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = Resident
        fields = [
            'first_name', 'last_name', 'status', 'date_of_birth', 
            'gender', 'marital_status', 'has_dnr',
            'referral_source', 'referral_facility', 'referred_by'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        required_custom_fields = {
            'ssn': 'SSN is required.',
            'referral_source': 'Referral Source is required.',
            'phone_primary': 'Primary Phone is required.',
            'emergency_first_name': 'Emergency Contact First Name is required.',
            'emergency_last_name': 'Emergency Contact Last Name is required.',
            'emergency_phone_primary': 'Emergency Contact Primary Phone is required.',
            'insurance_provider_name': 'Insurance Provider Name is required.'
        }
        
        for field, msg in required_custom_fields.items():
            val = cleaned_data.get(field)
            if not val or str(val).strip() == '':
                self.add_error(field, msg)
                
        # SSN validation
        ssn = cleaned_data.get('ssn')
        if ssn:
            import re
            if not re.match(r'^[\dX]{3}-[\dX]{2}-[\dX]{4}$', ssn, re.IGNORECASE):
                self.add_error('ssn', 'Invalid SSN format. Expected format: XXX-XX-XXXX.')
            else:
                # Uniqueness check
                from apps.residents.models import ResidentSensitiveInfo
                qs = ResidentSensitiveInfo.objects.filter(ssn_encrypted=ssn)
                if self.instance and self.instance.pk:
                    qs = qs.exclude(resident=self.instance)
                if qs.exists():
                    self.add_error('ssn', 'A resident with this SSN already exists.')

        # Policy Number validation
        policy_number = cleaned_data.get('policy_number')
        if policy_number:
            from apps.billing.models import ResidentInsurancePolicy
            qs = ResidentInsurancePolicy.objects.filter(policy_number_encrypted=policy_number)
            if self.instance and self.instance.pk:
                qs = qs.exclude(resident=self.instance)
            if qs.exists():
                self.add_error('policy_number', 'A resident with this Policy Number already exists.')
                
        # Resident duplicate check (first_name, last_name, dob)
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        dob = cleaned_data.get('date_of_birth')
        if first_name and last_name and dob:
            from apps.residents.models import Resident
            qs = Resident.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name,
                date_of_birth=dob
            )
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error(None, 'A resident with the same first name, last name, and date of birth already exists. Please verify before saving.')
                
        return cleaned_data
