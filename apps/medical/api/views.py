import csv
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.residents.models import Resident
from apps.medical.models import ResidentCareLevelHistory
from .serializers import ResidentCareLevelHistorySerializer

class ResidentCareLevelHistoryListView(generics.ListAPIView):
    serializer_class = ResidentCareLevelHistorySerializer

    def get_queryset(self):
        resident_id = self.kwargs.get('resident_id')
        return ResidentCareLevelHistory.objects.filter(resident_id=resident_id)

class ResidentCareLevelHistoryExportView(APIView):
    def get(self, request, resident_id):
        resident = get_object_or_404(Resident, id=resident_id)
        queryset = ResidentCareLevelHistory.objects.filter(resident=resident)
        
        # Always return CSV for simplicity in this implementation
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="loc_history_{resident_id}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Action', 'Previous Tier', 'New Tier', 'Actor', 'Note'])
        
        for history in queryset:
            actor_name = history.actor.get_full_name() if history.actor else "System"
            date_str = history.date.strftime("%m/%d/%Y %H:%M")
            writer.writerow([
                date_str,
                history.action,
                history.previous_tier or "",
                history.new_tier,
                actor_name,
                history.note or ""
            ])
            
        return response