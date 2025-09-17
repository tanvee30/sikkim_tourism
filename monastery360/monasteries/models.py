from django.db import models

from django.conf import settings


class Monastery(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)  # Later if you want geospatial, you can switch
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    established_year = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(blank=True)
    virtual_tour_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    # monasteries/models.py



class Archive(models.Model):
    title = models.CharField(max_length=200)  # Name of the archive item
    description = models.TextField()          # Detailed description
    image = models.ImageField(upload_to="archives/", blank=True, null=True)  # Image of manuscript/mural
    category = models.CharField(
        max_length=50,
        choices=[
            ("manuscript", "Manuscript"),
            ("mural", "Mural"),
            ("thangka", "Thangka Painting"),
            ("relic", "Relic"),
            ("other", "Other"),
        ],
        default="other"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Link to monastery (one monastery can have many archives)
    monastery = models.ForeignKey(
        "Monastery", on_delete=models.CASCADE, related_name="archives"
    )

    def __str__(self):
        return f"{self.title} ({self.monastery.name})"




class Monk(models.Model):
    name = models.CharField(max_length=100)
    monastery = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="monks/")

    def __str__(self):
        return self.name


class MonkSession(models.Model):
    monk = models.ForeignKey(Monk, on_delete=models.CASCADE, related_name="sessions")
    title = models.CharField(max_length=200)  # e.g., "Morning Meditation"
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(default=10)
    donation = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.monk.name}"


class MonkSessionApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    session = models.ForeignKey(MonkSession, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.email} -> {self.session.title}"



class MonasteryPanorama(models.Model):
    monastery = models.ForeignKey(Monastery, related_name='panoramas', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='panoramas/')
