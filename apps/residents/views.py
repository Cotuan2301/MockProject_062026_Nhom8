from django.shortcuts import render

def add_resident(request):
    return render(request, "residents/add_resident.html")


def resident_list(request):
    return render(request, "residents/list.html")