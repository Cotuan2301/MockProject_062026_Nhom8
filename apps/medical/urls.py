# pyrefly: ignore [missing-import]
from django.urls import path
from . import views

app_name = 'medical'
urlpatterns = [
    path('cost-billing/', views.billing_panel, name='cost_billing_panel'),
]