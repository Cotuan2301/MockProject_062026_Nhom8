from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('residents/', include(('apps.residents.urls', 'residents'), namespace='residents')),
    path('rooms/', include(('apps.rooms.urls', 'rooms'), namespace='rooms')),
    path('staff/', include(('apps.staff.urls', 'staff'), namespace='staff')),
    path('billing/', include(('apps.billing.urls', 'billing'), namespace='billing')),
    path('incidents/', include(('apps.incidents.urls', 'incidents'), namespace='incidents')),
    path('medical/', include(('apps.medical.urls', 'medical'), namespace='medical')),
]