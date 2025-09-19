from rest_framework import serializers
from .models import Monastery

from .models import Archive

from .models import Monk, MonkSession, MonkSessionApplication


class MonasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Monastery
        fields = '__all__'

# monasteries/serializers.py



class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = "__all__"



class MonkSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True)

    class Meta:
        model = Monk
        fields = "__all__"


class MonkSessionSerializer(serializers.ModelSerializer):
    monk = MonkSerializer(read_only=True)

    class Meta:
        model = MonkSession
        fields = "__all__"


class MonkSessionApplicationSerializer(serializers.ModelSerializer):
    session = MonkSessionSerializer(read_only=True)

    class Meta:
        model = MonkSessionApplication
        fields = "__all__"
        read_only_fields = ["user", "applied_at", "status"]

from rest_framework import serializers
from .models import Monastery, MonasteryVirtualTourImage

class MonasteryVirtualTourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonasteryVirtualTourImage
        fields = ["image"]

class MonasterySerializer(serializers.ModelSerializer):
    virtual_tour_images = MonasteryVirtualTourImageSerializer(many=True, read_only=True)

    class Meta:
        model = Monastery
        fields = ["id", "name", "description", "virtual_tour_images"]
