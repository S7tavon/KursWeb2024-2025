from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import City, Weather, Forecast
from import_export import resources
from import_export.admin import ImportExportMixin
from django.utils.html import format_html
from django.urls import reverse

# Ресурсы для django-import-export
class CityResource(resources.ModelResource):
    class Meta:
        model = City

    def get_export_queryset(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.filter(population__gte=100000)  # Пример кастомизации

    def dehydrate_name(self, city):
        return city.name.upper()  # Пример кастомизации

class WeatherResource(resources.ModelResource):
    class Meta:
        model = Weather

class ForecastResource(resources.ModelResource):
    class Meta:
        model = Forecast

# Админ для City
@admin.register(City)
class CityAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = CityResource
    list_display = ('name', 'country', 'population', 'weather_count')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    fieldsets = (
        (None, {
            'fields': ('name', 'country', 'population')
        }),
        ('Дополнительная информация', {
            'fields': ()
        }),
    )
    inlines = []
    
    def weather_count(self, obj):
        count = obj.weather.count()
        url = reverse("admin:weather_app_weather_changelist") + f"?city__id__exact={obj.id}"
        return format_html('<a href="{}">{}</a>', url, count)
    weather_count.short_description = 'Количество записей о погоде'

# Админ для Weather
@admin.register(Weather)
class WeatherAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = WeatherResource
    list_display = ('city', 'temperature', 'humidity', 'description', 'date')
    search_fields = ('city__name', 'description')
    list_filter = ('date', 'city')
    fieldsets = (
        (None, {
            'fields': ('city', 'temperature', 'humidity', 'description')
        }),
        ('Временные метки', {
            'fields': ('date',)
        }),
    )
    inlines = []

# Админ для Forecast
@admin.register(Forecast)
class ForecastAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = ForecastResource
    list_display = ('city', 'date', 'high_temp', 'low_temp', 'description')
    search_fields = ('city__name', 'description')
    list_filter = ('date', 'city')
    fieldsets = (
        (None, {
            'fields': ('city', 'date', 'high_temp', 'low_temp', 'description')
        }),
    )
    inlines = []
