from django.db import models
from simple_history.models import HistoricalRecords

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    population = models.PositiveIntegerField(null=True, blank=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.name}, {self.country}"

class Weather(models.Model):
    city = models.ForeignKey(City, related_name='weather', on_delete=models.CASCADE)
    temperature = models.FloatField()  # Температура в градусах Цельсия
    humidity = models.PositiveIntegerField()  # Влажность в процентах
    description = models.CharField(max_length=255)  # Описание погоды
    date = models.DateField(auto_now_add=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"Weather in {self.city.name} on {self.date}"

class Forecast(models.Model):
    city = models.ForeignKey(City, related_name='forecasts', on_delete=models.CASCADE)
    date = models.DateField()
    high_temp = models.FloatField()
    low_temp = models.FloatField()
    description = models.CharField(max_length=255)
    history = HistoricalRecords()
    
    class Meta:
        unique_together = ('city', 'date')
    
    def __str__(self):
        return f"Forecast for {self.city.name} on {self.date}"
