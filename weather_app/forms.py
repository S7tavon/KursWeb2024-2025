from django import forms
from .models import City, Weather, Forecast

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'country', 'population']

class WeatherForm(forms.ModelForm):
    class Meta:
        model = Weather
        fields = ['city', 'temperature', 'humidity', 'description']

class ForecastForm(forms.ModelForm):
    class Meta:
        model = Forecast
        fields = ['city', 'date', 'high_temp', 'low_temp', 'description']
