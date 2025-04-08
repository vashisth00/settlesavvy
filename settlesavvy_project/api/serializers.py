# api/serializers.py

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from accounts.models import RealtorProfile
from maps.models import Maps, Geographies, MapGeos, PointOfInterest
from factors.models import Factors, GeoFactors, MapFactors, MapFactorGeos

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone', 'is_realtor', 'preferred_city', 'preferred_state']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class RealtorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtorProfile
        fields = ['id', 'user', 'license_number', 'agency_name', 
                  'service_areas', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MapSerializer(serializers.ModelSerializer):
    center_latitude = serializers.FloatField(write_only=True)
    center_longitude = serializers.FloatField(write_only=True)
    
    class Meta:
        model = Maps
        fields = ['map_id', 'name', 'center_point', 'zoom_level', 
                  'created_stamp', 'last_updated', 'created_by',
                  'center_latitude', 'center_longitude']
        read_only_fields = ['map_id', 'created_stamp', 'last_updated', 'created_by']
    
    def create(self, validated_data):
        # Extract and remove the latitude and longitude
        latitude = validated_data.pop('center_latitude')
        longitude = validated_data.pop('center_longitude')
        
        # Create a point geometry from the latitude and longitude
        center_point = Point(longitude, latitude, srid=4326)
        validated_data['center_point'] = center_point
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Extract and remove the latitude and longitude if they exist
        latitude = validated_data.pop('center_latitude', None)
        longitude = validated_data.pop('center_longitude', None)
        
        # If both latitude and longitude are provided, update the center_point
        if latitude is not None and longitude is not None:
            center_point = Point(longitude, latitude, srid=4326)
            validated_data['center_point'] = center_point
        
        return super().update(instance, validated_data)


class GeographySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Geographies
        geo_field = "geometry"
        fields = ['geo_id', 'geo_type', 'name', 'namelsad', 'aland', 
                  'awater', 'intptlat', 'intptlon']
        read_only_fields = ['geo_id']


class MapGeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapGeos
        fields = ['map_geo_id', 'map', 'geo', 'name']
        read_only_fields = ['map_geo_id']


class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factors
        fields = ['factor_id', 'name', 'description', 'source', 
                  'default_scoring_strategy', 'category', 
                  'display_name', 'units', 'is_active']
        read_only_fields = ['factor_id']


class GeoFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoFactors
        fields = ['geo_factor_id', 'factor', 'geo', 'value', 
                  'last_updated', 'needs_fetch']
        read_only_fields = ['geo_factor_id', 'last_updated']


class MapFactorSerializer(serializers.ModelSerializer):
    factor_name = serializers.CharField(source='factor.name', read_only=True)
    factor_description = serializers.CharField(source='factor.description', read_only=True)
    factor_units = serializers.CharField(source='factor.units', read_only=True)
    
    class Meta:
        model = MapFactors
        fields = [
            'map_factor_id', 'map', 'factor', 'weight', 
            'scoring_strategy', 'filter_strategy', 
            'score_tipping_1', 'score_tipping_2', 
            'filter_tipping_1', 'filter_tipping_2', 
            'created_stamp', 'is_active',
            'factor_name', 'factor_description', 'factor_units'
        ]
        read_only_fields = ['map_factor_id', 'created_stamp']


class MapFactorGeoSerializer(serializers.ModelSerializer):
    factor_name = serializers.CharField(source='map_factor.factor.name', read_only=True)
    geo_name = serializers.CharField(source='map_geo.name', read_only=True)
    
    class Meta:
        model = MapFactorGeos
        fields = [
            'uuid', 'geo_factor', 'map_factor', 'map_geo', 
            'aggregate_score', 'raw_value', 'is_filtered_out',
            'factor_name', 'geo_name'
        ]
        read_only_fields = ['uuid']


class PointOfInterestSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    
    class Meta:
        model = PointOfInterest
        fields = [
            'poi_id', 'map', 'name', 'description', 
            'location', 'poi_type', 'created_at',
            'latitude', 'longitude'
        ]
        read_only_fields = ['poi_id', 'created_at', 'location']