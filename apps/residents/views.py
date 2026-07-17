import datetime
# pyrefly: ignore [missing-import]
from django.shortcuts import render
from .models import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

def add_resident(request):
    return render(request, "residents/add_resident.html")


# Resident detail
class ResidentDetail(View):

    def get(self, request, pk):
        resident = Resident.objects.get(pk=pk)
        return render(request, "residents/resident_detail.html", {
            'resident': resident
        })

