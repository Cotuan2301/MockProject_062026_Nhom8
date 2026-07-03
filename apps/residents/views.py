from django.shortcuts import render

def pre_admission_screening(request):
    return render(request, 'residents/pre_admission_screening.html')