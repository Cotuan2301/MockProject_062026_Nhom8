from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.residents.models import Resident
from .serializers import ResidentDetailSerializer

class ResidentDetailAPIView(APIView):
    def get(self, request, pk, format=None):
        resident = get_object_or_404(
            Resident.objects.select_related(
                'address', 
                'residentsensitiveinfo',
                'bed__room'
            ).prefetch_related(
                'residentcontact_set__contact',
                'residentinsurancepolicy_set__insurance_provider', 
                'residentcarelevelhistory_set__care_level',
                'admission_set',
                'clinicalrecord_set',
                'assessment_set__confirmed_care_level'
            ), 
            pk=pk
        )
        
        serializer = ResidentDetailSerializer(resident)
        return Response(serializer.data)

