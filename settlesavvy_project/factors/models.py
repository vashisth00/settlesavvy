# factors/models.py

import uuid
from django.db import models
from django.utils import timezone
from maps.models import Maps, Geographies, MapGeos


class Factors(models.Model):
    factor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    source = models.CharField(max_length=255)
    default_scoring_strategy = models.CharField(max_length=50)
    category = models.CharField(max_length=100, blank=True, null=True)  # e.g., Safety, Education, etc.
    display_name = models.CharField(max_length=255, blank=True, null=True)  # User-friendly name
    units = models.CharField(max_length=50, blank=True, null=True)  # e.g., minutes, percent, dollars
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Factors"


class GeoFactors(models.Model):
    geo_factor_id = models.AutoField(primary_key=True)
    factor = models.ForeignKey(Factors, on_delete=models.CASCADE, related_name='geo_factors')
    geo = models.ForeignKey(Geographies, on_delete=models.CASCADE, related_name='factor_values')
    value = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)
    needs_fetch = models.BooleanField(default=True)

    class Meta:
        unique_together = ('factor', 'geo')
        verbose_name_plural = "Geo Factors"

    def __str__(self):
        return f"{self.factor.name} - {self.geo.name}"


class MapFactors(models.Model):
    SCORING_STRATEGIES = [
        ('higher_better', 'Higher is Better'),
        ('lower_better', 'Lower is Better'),
        ('closer_to_value', 'Closer to Value is Better'),
        ('farther_from_value', 'Farther from Value is Better'),
        ('no_scoring', 'No Scoring'),
    ]
    
    FILTER_STRATEGIES = [
        ('above_threshold', 'Above Threshold'),
        ('below_threshold', 'Below Threshold'),
        ('between_thresholds', 'Between Thresholds'),
        ('outside_thresholds', 'Outside Thresholds'),
        ('no_filter', 'No Filter'),
    ]
    
    map_factor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    map = models.ForeignKey(Maps, on_delete=models.CASCADE, related_name='map_factors')
    factor = models.ForeignKey(Factors, on_delete=models.CASCADE, related_name='map_factors')
    weight = models.FloatField()
    scoring_strategy = models.CharField(max_length=50, choices=SCORING_STRATEGIES, default='no_scoring')
    filter_strategy = models.CharField(max_length=50, choices=FILTER_STRATEGIES, default='no_filter')
    score_tipping_1 = models.FloatField(null=True, blank=True)
    score_tipping_2 = models.FloatField(null=True, blank=True)
    filter_tipping_1 = models.FloatField(null=True, blank=True)
    filter_tipping_2 = models.FloatField(null=True, blank=True)
    created_stamp = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.factor.name} - {self.map.name}"
    
    class Meta:
        verbose_name_plural = "Map Factors"
        unique_together = ('map', 'factor')


class MapFactorGeos(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    geo_factor = models.ForeignKey(GeoFactors, on_delete=models.CASCADE, related_name='map_factor_geos')
    map_factor = models.ForeignKey(MapFactors, on_delete=models.CASCADE, related_name='map_factor_geos')
    map_geo = models.ForeignKey(MapGeos, on_delete=models.CASCADE, related_name='map_factor_geos')
    aggregate_score = models.FloatField()
    raw_value = models.FloatField()  # Store the original value before scoring
    is_filtered_out = models.BooleanField(default=False)  # If this area was filtered out

    def __str__(self):
        return f"{self.map_factor.factor.name} - {self.map_geo.name}"
    
    class Meta:
        verbose_name_plural = "Map Factor Geos"
        unique_together = ('geo_factor', 'map_factor', 'map_geo')