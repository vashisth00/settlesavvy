import uuid
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils import timezone
from settlesavvy_accounts.models import User


class Maps(models.Model):
    map_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_stamp = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    center_point = gis_models.PointField(geography=True)
    zoom_level = models.FloatField()
    
    # Add a field to track the user who created the map
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maps', null=True)

    def __str__(self):
        return f"{self.name}"


class Geographies(models.Model):
    geo_id = models.CharField(primary_key=True, max_length=20, default='0000000')
    geo_type = models.CharField(max_length=50, default='unspecified')
    name = models.CharField(max_length=255, default='Unnamed')
    namelsad = models.CharField(max_length=255, default='Unnamed Area')
    aland = models.BigIntegerField(default=0)
    awater = models.BigIntegerField(default=0)
    intptlat = models.DecimalField(max_digits=9, decimal_places=7, default=0.0)
    intptlon = models.DecimalField(max_digits=10, decimal_places=7, default=0.0)
    geometry = gis_models.MultiPolygonField(srid=4326)  # Explicitly set SRID and geometry type


    def __str__(self):
        return f"{self.name} ({self.geo_id})"

    class Meta:
        verbose_name_plural = "Geographies"


class MapGeos(models.Model):
    map_geo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    map = models.ForeignKey(Maps, on_delete=models.CASCADE)
    geo = models.ForeignKey(Geographies, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.map.name}"


class Factors(models.Model):
    factor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    source = models.CharField(max_length=255)
    default_scoring_strategy = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class GeoFactors(models.Model):
    geo_factor_id = models.AutoField(primary_key=True)
    factor = models.ForeignKey(Factors, on_delete=models.CASCADE)
    geo = models.ForeignKey(Geographies, on_delete=models.CASCADE)
    value = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)
    needs_fetch = models.BooleanField(default=True)

    class Meta:
        unique_together = ('factor', 'geo')

    def __str__(self):
        return f"{self.factor.name} - {self.geo.name}"


class MapFactors(models.Model):
    map_factor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    map = models.ForeignKey(Maps, on_delete=models.CASCADE)
    factor = models.ForeignKey(Factors, on_delete=models.CASCADE)
    weight = models.FloatField()
    scoring_strategy = models.CharField(max_length=50, default='no_scoring')
    filter_strategy = models.CharField(max_length=50, default='no_filter')
    score_tipping_1 = models.FloatField(null=True, blank=True)
    score_tipping_2 = models.FloatField(null=True, blank=True)
    filter_tipping_1 = models.FloatField(null=True, blank=True)
    filter_tipping_2 = models.FloatField(null=True, blank=True)
    created_stamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.factor.name} - {self.map.name}"


class MapFactorGeos(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    geo_factor = models.ForeignKey(GeoFactors, on_delete=models.CASCADE)
    map_factor = models.ForeignKey(MapFactors, on_delete=models.CASCADE)
    map_geo = models.ForeignKey(MapGeos, on_delete=models.CASCADE)
    aggregate_score = models.FloatField()

    def __str__(self):
        return f"{self.map_factor.factor.name} - {self.map_geo.name}"