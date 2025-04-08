# settlesavvy_api/serializers.py

from rest_framework import serializers
from settlesavvy_accounts.models import User

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_realtor')
        read_only_fields = ('id',)

# Map serializer - simple version that doesn't depend on a database model
class MapSerializer(serializers.Serializer):
    map_id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)
    zoom_level = serializers.FloatField(default=10)
    created_stamp = serializers.DateTimeField(read_only=True)
    last_updated = serializers.DateTimeField(read_only=True)
    
    def validate(self, data):
        """
        Check that latitude and longitude are valid if provided
        """
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is not None and (latitude < -90 or latitude > 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90")
        
        if longitude is not None and (longitude < -180 or longitude > 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180")
        
        return data