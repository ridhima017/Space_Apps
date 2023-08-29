from django.db import models

class MapPoint(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def _str_(self):
        return self.name
