from rest_framework import viewsets
from .models import Monastery
from .serializers import MonasterySerializer
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Monastery


from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from .models import Monk, MonkSession, MonkSessionApplication
from .serializers import MonkSerializer, MonkSessionSerializer, MonkSessionApplicationSerializer



from .models import Archive
from .serializers import ArchiveSerializer

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
    



class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

class MonasteryArchivesView(APIView):
    def get(self, request, pk):
        monastery = Monastery.objects.get(pk=pk)
        archives = monastery.archives.all()
        serializer = ArchiveSerializer(archives, many=True)
        return Response(serializer.data)




class MonkViewSet(viewsets.ModelViewSet):
    queryset = Monk.objects.all()
    serializer_class = MonkSerializer


class MonkSessionViewSet(viewsets.ModelViewSet):
    queryset = MonkSession.objects.all()
    serializer_class = MonkSessionSerializer

    # List sessions for a specific monk
    @action(detail=True, methods=["get"])
    def monk_sessions(self, request, pk=None):
        sessions = MonkSession.objects.filter(monk_id=pk)
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)


class MonkSessionApplicationViewSet(viewsets.ModelViewSet):
    queryset = MonkSessionApplication.objects.all()
    serializer_class = MonkSessionApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # List only logged-in user's applications
    @action(detail=False, methods=["get"])
    def my_applications(self, request):
        apps = MonkSessionApplication.objects.filter(user=request.user)
        serializer = self.get_serializer(apps, many=True)
        return Response(serializer.data)

