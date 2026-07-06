from django.shortcuts import render

def activate_account(request):
    return render(request, "accounts/activate_account.html")