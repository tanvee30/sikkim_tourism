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
from .models import Market


class MarketSerializer(serializers.ModelSerializer):
    static_map_url = serializers.SerializerMethodField()

    class Meta:
        model = Market
        fields = ["id", "name", "description", "location", "latitude", "longitude", "image", "static_map_url"]

    def get_static_map_url(self, obj):
        from django.conf import settings
        return (
            f"https://maps.googleapis.com/maps/api/staticmap?"
            f"center={obj.latitude},{obj.longitude}"
            f"&zoom=15&size=600x300&markers=color:red%7C{obj.latitude},{obj.longitude}"
            f"&key={settings.GOOGLE_STATIC_MAPS_API_KEY}"
        )
