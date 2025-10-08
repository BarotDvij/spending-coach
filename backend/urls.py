from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),       # root-level endpoints
    path('api/', include('core.urls')),   # prefixed endpoints
]
