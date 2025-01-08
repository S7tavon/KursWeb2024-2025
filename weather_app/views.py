from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import City, Weather, Forecast
from .serializers import CitySerializer, WeatherSerializer, ForecastSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CityForm, WeatherForm, ForecastForm
from django.core.paginator import Paginator

# API ViewSets
class CityViewSet(viewsets.ModelViewSet):
    """
    API для городов.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'country']
    search_fields = ['name', 'country']
    
    # Дополнительный метод: получение последних 5 городов
    @action(methods=['GET'], detail=False)
    def recent_cities(self, request):
        recent = self.queryset.order_by('-id')[:5]
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)
    
    # Дополнительный метод: обновление населения города
    @action(methods=['POST'], detail=True)
    def update_population(self, request, pk=None):
        city = self.get_object()
        population = request.data.get('population')
        if population is not None and population.isdigit():
            city.population = int(population)
            city.save()
            return Response({'status': 'Население обновлено.'})
        return Response({'error': 'Некорректное значение населения.'}, status=status.HTTP_400_BAD_REQUEST)

class WeatherViewSet(viewsets.ModelViewSet):
    """
    API для текущей погоды.
    """
    queryset = Weather.objects.select_related('city').all()
    serializer_class = WeatherSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city__name', 'humidity']
    search_fields = ['description']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Пример сложного запроса: (temperature > 20 AND humidity < 50) OR NOT description contains 'rain'
        q1 = Q(temperature__gt=20) & Q(humidity__lt=50)
        q2 = ~Q(description__icontains='rain')
        return queryset.filter(q1 | q2)
    
    # Дополнительный метод: получить погодные условия за конкретный день
    @action(methods=['GET'], detail=False)
    def by_date(self, request):
        date = request.query_params.get('date')
        if date:
            weather = self.queryset.filter(date=date)
            serializer = self.get_serializer(weather, many=True)
            return Response(serializer.data)
        return Response({'error': 'Дата не указана.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Дополнительный метод: обновить описание погоды
    @action(methods=['POST'], detail=True)
    def update_description(self, request, pk=None):
        weather = self.get_object()
        description = request.data.get('description')
        if description:
            weather.description = description
            weather.save()
            return Response({'status': 'Описание погоды обновлено.'})
        return Response({'error': 'Описание не предоставлено.'}, status=status.HTTP_400_BAD_REQUEST)

class ForecastViewSet(viewsets.ModelViewSet):
    """
    API для прогнозов погоды.
    """
    queryset = Forecast.objects.select_related('city').all()
    serializer_class = ForecastSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city__name', 'date']
    search_fields = ['description']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Пример сложного запроса: (high_temp > 25 AND low_temp > 15) OR NOT description contains 'cloud'
        q1 = Q(high_temp__gt=25) & Q(low_temp__gt=15)
        q2 = ~Q(description__icontains='cloud')
        return queryset.filter(q1 | q2)
    
    # Дополнительный метод: получить прогнозы на определенный период
    @action(methods=['GET'], detail=False)
    def period(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            forecasts = self.queryset.filter(date__range=[start_date, end_date])
            serializer = self.get_serializer(forecasts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Необходимо указать start_date и end_date.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Дополнительный метод: обновить прогноз
    @action(methods=['POST'], detail=True)
    def update_forecast(self, request, pk=None):
        forecast = self.get_object()
        data = request.data
        serializer = self.get_serializer(forecast, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Прогноз обновлен.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Веб Представления
def home(request):
    return render(request, 'weather_app/home.html')

# City Views
def city_list(request):
    cities = City.objects.all()
    paginator = Paginator(cities, 10)  # 10 городов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'weather_app/city_list.html', {'page_obj': page_obj})

def city_detail(request, pk):
    city = get_object_or_404(City, pk=pk)
    weather = city.weather.all()
    forecasts = city.forecasts.all()
    return render(request, 'weather_app/city_detail.html', {'city': city, 'weather': weather, 'forecasts': forecasts})

def city_create(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('city_list')
    else:
        form = CityForm()
    return render(request, 'weather_app/city_form.html', {'form': form})

def city_update(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('city_detail', pk=pk)
    else:
        form = CityForm(instance=city)
    return render(request, 'weather_app/city_form.html', {'form': form})

def city_delete(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.method == 'POST':
        city.delete()
        return redirect('city_list')
    return render(request, 'weather_app/city_confirm_delete.html', {'city': city})

# Weather Views
def weather_list(request):
    weathers = Weather.objects.all()
    paginator = Paginator(weathers, 10)  # 10 записей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'weather_app/weather_list.html', {'page_obj': page_obj})

def weather_detail(request, pk):
    weather = get_object_or_404(Weather, pk=pk)
    return render(request, 'weather_app/weather_detail.html', {'weather': weather})

def weather_create(request):
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('weather_list')
    else:
        form = WeatherForm()
    return render(request, 'weather_app/weather_form.html', {'form': form})

def weather_update(request, pk):
    weather = get_object_or_404(Weather, pk=pk)
    if request.method == 'POST':
        form = WeatherForm(request.POST, instance=weather)
        if form.is_valid():
            form.save()
            return redirect('weather_detail', pk=pk)
    else:
        form = WeatherForm(instance=weather)
    return render(request, 'weather_app/weather_form.html', {'form': form})

def weather_delete(request, pk):
    weather = get_object_or_404(Weather, pk=pk)
    if request.method == 'POST':
        weather.delete()
        return redirect('weather_list')
    return render(request, 'weather_app/weather_confirm_delete.html', {'weather': weather})

# Forecast Views
def forecast_list(request):
    forecasts = Forecast.objects.all()
    paginator = Paginator(forecasts, 10)  # 10 прогнозов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'weather_app/forecast_list.html', {'page_obj': page_obj})

def forecast_detail(request, pk):
    forecast = get_object_or_404(Forecast, pk=pk)
    return render(request, 'weather_app/forecast_detail.html', {'forecast': forecast})

def forecast_create(request):
    if request.method == 'POST':
        form = ForecastForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forecast_list')
    else:
        form = ForecastForm()
    return render(request, 'weather_app/forecast_form.html', {'form': form})

def forecast_update(request, pk):
    forecast = get_object_or_404(Forecast, pk=pk)
    if request.method == 'POST':
        form = ForecastForm(request.POST, instance=forecast)
        if form.is_valid():
            form.save()
            return redirect('forecast_detail', pk=pk)
    else:
        form = ForecastForm(instance=forecast)
    return render(request, 'weather_app/forecast_form.html', {'form': form})

def forecast_delete(request, pk):
    forecast = get_object_or_404(Forecast, pk=pk)
    if request.method == 'POST':
        forecast.delete()
        return redirect('forecast_list')
    return render(request, 'weather_app/forecast_confirm_delete.html', {'forecast': forecast})
