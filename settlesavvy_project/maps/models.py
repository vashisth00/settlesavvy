# maps/models.py

import uuid
from django.db import models
# from django.contrib.gis.db import models as gis_models
from django.utils import timezone
from accounts.models import User


class Maps(models.Model):
    map_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_stamp = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    # center_point = gis_models.PointField(geography=True)
    center_lat = models.FloatField(default=0.0)
    center_lng = models.FloatField(default=0.0)
    zoom_level = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_maps')

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Maps"


class Geographies(models.Model):
    geo_id = models.CharField(primary_key=True, max_length=20, default='0000000')
    geo_type = models.CharField(max_length=50, default='unspecified')
    name = models.CharField(max_length=255, default='Unnamed')
    namelsad = models.CharField(max_length=255, default='Unnamed Area')
    aland = models.BigIntegerField(default=0)
    awater = models.BigIntegerField(default=0)
    intptlat = models.DecimalField(max_digits=9, decimal_places=7, default=0.0)
    intptlon = models.DecimalField(max_digits=10, decimal_places=7, default=0.0)
    # geometry = gis_models.MultiPolygonField(srid=4326)  # Explicitly set SRID and geometry type
    geometry_json = models.TextField(null=True, blank=True)  # Store GeoJSON as text


    def __str__(self):
        return f"{self.name} ({self.geo_id})"

    class Meta:
        verbose_name_plural = "Geographies"


class MapGeos(models.Model):
    map_geo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    map = models.ForeignKey(Maps, on_delete=models.CASCADE, related_name='map_geos')
    geo = models.ForeignKey(Geographies, on_delete=models.CASCADE, related_name='geo_maps')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.map.name}"
    
    class Meta:
        verbose_name_plural = "Map Geos"
        unique_together = ('map', 'geo')


class PointOfInterest(models.Model):
    """Model for storing specific points of interest on a map (e.g., workplace, school)"""
    poi_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    map = models.ForeignKey(Maps, on_delete=models.CASCADE, related_name='points_of_interest')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # location = gis_models.PointField(geography=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255, blank=True, null=True)
    poi_type = models.CharField(max_length=50)  # e.g., work, school, family
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.poi_type}) - {self.map.name}"