from django.contrib import admin
from django.urls import path, include
from apps.accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', accounts_views.login_view, name='login'),
    path('', accounts_views.login_view, name='home'),
    path('residents/', include('apps.residents.urls')),
]
