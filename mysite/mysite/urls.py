from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webexamples/', include('webexamples.urls')),
    path('', include('mainApp.urls')),
    path('accounts/', include('django.contrib.auth.urls'))
]
