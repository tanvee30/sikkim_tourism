from rest_framework import serializers
from .models import Monastery

class MonasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Monastery
        fields = '_all_'


from rest_framework import serializers
from .models import Monastery
from .models import Festival


class FestivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival
        fields = '_all_'