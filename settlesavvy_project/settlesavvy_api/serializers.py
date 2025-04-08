# settlesavvy_api/serializers.py

from rest_framework import serializers
from settlesavvy_accounts.models import User

# Simple serializer just to get started
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_realtor')
        read_only_fields = ('id',)

# Placeholder for map serializer
class MapSerializer(serializers.Serializer):
    map_id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    created_stamp = serializers.DateTimeField(read_only=True)
    last_updated = serializers.DateTimeField(read_only=True)