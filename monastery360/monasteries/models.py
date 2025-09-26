from django.db import models

class Monastery(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)  # Later use GeoDjango
    established_year = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(blank=True)

    def _str_(self):
        return self.name
    
class Festival(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    image_url = models.URLField(blank=True)
    monastery = models.ForeignKey(
        Monastery,
        on_delete=models.CASCADE,
        related_name='festivals'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-start_date", "name"]
    
    def __str__(self):
        return f"{self.name} ({self.monastery.name})"