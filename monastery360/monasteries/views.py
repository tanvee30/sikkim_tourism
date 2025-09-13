from rest_framework import viewsets
from .models import Monastery
from .serializers import MonasterySerializer
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Monastery

class MonasteryViewSet(viewsets.ModelViewSet):
    queryset = Monastery.objects.all()
    serializer_class = MonasterySerializer



@api_view(["GET"])
def monastery_weather(request, pk):
    try:
        monastery = Monastery.objects.get(pk=pk)
        api_key = settings.OPENWEATHER_API_KEY
        if not api_key:
            return Response({"error": "Missing OpenWeather API key"}, status=500)

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={monastery.latitude}&lon={monastery.longitude}&appid={api_key}&units=metric"
        r = requests.get(url)
        data = r.json()

        if "main" not in data:  # API error
            return Response({"error": data.get("message", "Invalid response from API")}, status=500)

        return Response({
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
        })
    except Monastery.DoesNotExist:
        return Response({"error": "Monastery not found"}, status=404)
