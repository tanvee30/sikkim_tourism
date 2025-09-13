from rest_framework import serializers
from .models import Monastery

class MonasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Monastery
        fields = '__all__'
