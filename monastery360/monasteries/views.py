from rest_framework import viewsets
from .models import Monastery
from .serializers import MonasterySerializer

class MonasteryViewSet(viewsets.ModelViewSet):
    queryset = Monastery.objects.all()
    serializer_class = MonasterySerializer