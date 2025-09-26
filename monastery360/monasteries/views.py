from rest_framework import viewsets
from .models import Monastery
from .serializers import MonasterySerializer

class MonasteryViewSet(viewsets.ModelViewSet):
    queryset = Monastery.objects.all()
    serializer_class = MonasterySerializer


from rest_framework import viewsets
from .models import Monastery, Festival
from .serializers import MonasterySerializer, FestivalSerializer



class FestivalViewSet(viewsets.ModelViewSet):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer