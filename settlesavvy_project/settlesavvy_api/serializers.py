# settlesavvy_api/serializers.py

from rest_framework import serializers
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point
from settlesavvy_accounts.models import User
from settlesavvy_core.models import Maps, Geographies, MapGeos, Factors, GeoFactors, MapFactors, MapFactorGeos

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_realtor')
        read_only_fields = ('id',)

# Map serializer
class MapSerializer(serializers.ModelSerializer):
    """Serializer for Maps model"""
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    
    class Meta:
        model = Maps
        fields = ('map_id', 'name', 'created_stamp', 'last_updated', 'center_point', 
                  'zoom_level', 'created_by', 'latitude', 'longitude')
        read_only_fields = ('map_id', 'created_stamp', 'last_updated', 'center_point')
        extra_kwargs = {
            'center_point': {'required': False}  # Make center_point not required in validation
        }
    
    def validate(self, data):
        """
        Check that latitude and longitude are valid
        """
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is None:
            raise serializers.ValidationError({"latitude": "This field is required."})
        
        if longitude is None:
            raise serializers.ValidationError({"longitude": "This field is required."})
        
        if latitude < -90 or latitude > 90:
            raise serializers.ValidationError({"latitude": "Latitude must be between -90 and 90"})
        
        if longitude < -180 or longitude > 180:
            raise serializers.ValidationError({"longitude": "Longitude must be between -180 and 180"})
        
        return data
    
    def create(self, validated_data):
        """Create a new map with the given data"""
        # Extract latitude and longitude
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')
        
        # Create Point object
        center_point = Point(longitude, latitude, srid=4326)
        validated_data['center_point'] = center_point
        
        # Add the current user as the creator if available
        if 'request' in self.context and self.context['request'].user.is_authenticated:
            validated_data['created_by'] = self.context['request'].user
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update the map with the given data"""
        # Extract latitude and longitude
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        
        # If latitude and longitude are provided, update center_point
        if latitude is not None and longitude is not None:
            validated_data['center_point'] = Point(longitude, latitude, srid=4326)
        
        return super().update(instance, validated_data)

class GeographySerializer(GeoFeatureModelSerializer):
    """Serializer for Geographies model"""
    class Meta:
        model = Geographies
        geo_field = 'geometry'
        fields = ('geo_id', 'geo_type', 'name', 'namelsad', 'aland', 'awater', 'intptlat', 'intptlon')

class MapGeoSerializer(serializers.ModelSerializer):
    """Serializer for MapGeos model"""
    class Meta:
        model = MapGeos
        fields = '__all__'

class FactorSerializer(serializers.ModelSerializer):
    """Serializer for Factors model"""
    class Meta:
        model = Factors
        fields = '__all__'

class GeoFactorSerializer(serializers.ModelSerializer):
    """Serializer for GeoFactors model"""
    class Meta:
        model = GeoFactors
        fields = '__all__'

class MapFactorSerializer(serializers.ModelSerializer):
    """Serializer for MapFactors model"""
    factor_name = serializers.CharField(source='factor.name', read_only=True)
    
    class Meta:
        model = MapFactors
        fields = ('map_factor_id', 'map', 'factor', 'factor_name', 'weight', 
                  'scoring_strategy', 'filter_strategy', 
                  'score_tipping_1', 'score_tipping_2',
                  'filter_tipping_1', 'filter_tipping_2', 'created_stamp')
        read_only_fields = ('map_factor_id', 'created_stamp')

class MapFactorGeoSerializer(serializers.ModelSerializer):
    """Serializer for MapFactorGeos model"""
    class Meta:
        model = MapFactorGeos
        fields = '__all__'

class NeighborhoodScoreSerializer(serializers.Serializer):
    """Serializer for neighborhood scores"""
    geo_id = serializers.CharField()
    name = serializers.CharField()
    score = serializers.FloatField()
    is_filtered = serializers.BooleanField(default=False)
    geometry = serializers.JSONField()