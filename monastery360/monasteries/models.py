from django.db import models

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
