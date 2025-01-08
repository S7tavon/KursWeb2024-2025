from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('weather_app.urls')),  # API маршруты
    path('', include('weather_app.web_urls')),  # Веб-маршруты
]
