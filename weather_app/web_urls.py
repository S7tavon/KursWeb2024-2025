from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # City URLs
    path('cities/', views.city_list, name='city_list'),
    path('cities/create/', views.city_create, name='city_create'),
    path('cities/<int:pk>/', views.city_detail, name='city_detail'),
    path('cities/<int:pk>/update/', views.city_update, name='city_update'),
    path('cities/<int:pk>/delete/', views.city_delete, name='city_delete'),
    
    # Weather URLs
    path('weather/', views.weather_list, name='weather_list'),
    path('weather/create/', views.weather_create, name='weather_create'),
    path('weather/<int:pk>/', views.weather_detail, name='weather_detail'),
    path('weather/<int:pk>/update/', views.weather_update, name='weather_update'),
    path('weather/<int:pk>/delete/', views.weather_delete, name='weather_delete'),
    
    # Forecast URLs
    path('forecasts/', views.forecast_list, name='forecast_list'),
    path('forecasts/create/', views.forecast_create, name='forecast_create'),
    path('forecasts/<int:pk>/', views.forecast_detail, name='forecast_detail'),
    path('forecasts/<int:pk>/update/', views.forecast_update, name='forecast_update'),
    path('forecasts/<int:pk>/delete/', views.forecast_delete, name='forecast_delete'),
]
