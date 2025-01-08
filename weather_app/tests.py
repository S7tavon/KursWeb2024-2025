from django.test import TestCase
from .models import City, Weather, Forecast

class CityModelTest(TestCase):
    def setUp(self):
        City.objects.create(name="Moscow", country="Russia", population=11920000)

    def test_city_creation(self):
        city = City.objects.get(name="Moscow")
        self.assertEqual(city.country, "Russia")
        self.assertEqual(city.population, 11920000)

class WeatherModelTest(TestCase):
    def setUp(self):
        city = City.objects.create(name="New York", country="USA", population=8419000)
        Weather.objects.create(city=city, temperature=25.5, humidity=60, description="Sunny")

    def test_weather_creation(self):
        weather = Weather.objects.get(city__name="New York")
        self.assertEqual(weather.temperature, 25.5)
        self.assertEqual(weather.humidity, 60)
        self.assertEqual(weather.description, "Sunny")

class ForecastModelTest(TestCase):
    def setUp(self):
        city = City.objects.create(name="Tokyo", country="Japan", population=13960000)
        Forecast.objects.create(city=city, date="2024-12-10", high_temp=28.0, low_temp=18.0, description="Partly Cloudy")

    def test_forecast_creation(self):
        forecast = Forecast.objects.get(city__name="Tokyo")
        self.assertEqual(forecast.high_temp, 28.0)
        self.assertEqual(forecast.low_temp, 18.0)
        self.assertEqual(forecast.description, "Partly Cloudy")
