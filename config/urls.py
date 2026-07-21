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

    path('billing/', include('apps.billing.urls')),
    path('medical/', include('apps.medical.urls')),
    path('residents/', include('apps.residents.urls')),
    path('rooms/', include('apps.rooms.urls')),
    path('staff/', include('apps.staff.urls')),

    path('care-planning/', include('apps.care_planning.urls')),

    # path('incidents/', include('apps.incidents.urls')),
    path('api/v1/residents/', include('apps.residents.api.urls')),

    path('api/v1/medical/', include('apps.medical.api.urls')),

    path('incidents/', include('apps.incidents.urls')),
    
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

