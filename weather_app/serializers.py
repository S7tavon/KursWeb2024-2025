from rest_framework import serializers
from .models import City, Weather, Forecast

class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        if data['high_temp'] < data['low_temp']:
            raise serializers.ValidationError("Максимальная температура не может быть ниже минимальной.")
        return data

class WeatherSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    
    class Meta:
        model = Weather
        fields = '__all__'
        read_only_fields = ['id', 'date']

    def validate_temperature(self, value):
        if value < -100 or value > 60:
            raise serializers.ValidationError("Температура должна быть в диапазоне от -100 до 60 градусов Цельсия.")
        return value

class CitySerializer(serializers.ModelSerializer):
    weather = WeatherSerializer(many=True, read_only=True)
    forecasts = ForecastSerializer(many=True, read_only=True)
    
    class Meta:
        model = City
        fields = '__all__'
        read_only_fields = ['id']
    
    def validate_name(self, value):
        if 'test' in value.lower():
            raise serializers.ValidationError("Название города не может содержать слово 'test'.")
        return value
