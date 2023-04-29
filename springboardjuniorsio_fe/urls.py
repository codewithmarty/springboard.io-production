from django.contrib import admin
from django.urls import path, include
from core.views import front

urlpatterns = [
    path('', front, name="front"),
    path('api/', include('main_app.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
