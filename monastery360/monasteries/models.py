from django.db import models

class Monastery(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)  # Later use GeoDjango
    established_year = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(blank=True)

    def _str_(self):
        return self.name