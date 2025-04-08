# settlesavvy_api/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
import json
import uuid
from datetime import datetime

from settlesavvy_accounts.models import User
from .serializers import MapSerializer

# In-memory storage for maps (temporary solution until we have a database model)
MAPS = []

# Custom login view
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_401_UNAUTHORIZED)
    
    # Get or create a token
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_realtor': user.is_realtor
        }
    })

# Registration view
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not email or not password:
        return Response({'error': 'Please provide username, email, and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=request.data.get('first_name', ''),
        last_name=request.data.get('last_name', ''),
        phone=request.data.get('phone', ''),
        is_realtor=request.data.get('is_realtor', False),
        preferred_city=request.data.get('preferred_city', ''),
        preferred_state=request.data.get('preferred_state', '')
    )
    
    # Create token
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_realtor': user.is_realtor
        }
    }, status=status.HTTP_201_CREATED)

# Updated MapViewSet that supports POST (create) operations and stores maps in memory
class MapViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, and creating maps.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        # Return all maps from our in-memory storage
        return Response(MAPS)
    
    def retrieve(self, request, pk=None):
        # Find the map with the given ID
        for map_data in MAPS:
            if map_data['map_id'] == pk:
                return Response(map_data)
        
        # If no map is found, return 404
        return Response({"error": "Map not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        # Extract data from request
        name = request.data.get('name')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        zoom_level = request.data.get('zoom_level', 10)
        
        # Validate required fields
        if not name:
            return Response({"error": "Map name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new map object
        current_time = datetime.now().isoformat()
        map_id = str(uuid.uuid4())  # Generate a unique ID
        
        new_map = {
            "map_id": map_id,
            "name": name,
            "created_stamp": current_time,
            "last_updated": current_time,
            "center_point": {
                "type": "Point",
                "coordinates": [longitude if longitude else 0, latitude if latitude else 0]
            },
            "zoom_level": zoom_level
        }
        
        # Add to in-memory storage
        MAPS.append(new_map)
        
        return Response(new_map, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        # Find the map with the given ID
        for i, map_data in enumerate(MAPS):
            if map_data['map_id'] == pk:
                # Update fields that are provided
                if 'name' in request.data:
                    MAPS[i]['name'] = request.data['name']
                
                if 'latitude' in request.data and 'longitude' in request.data:
                    MAPS[i]['center_point']['coordinates'] = [
                        request.data['longitude'],
                        request.data['latitude']
                    ]
                
                if 'zoom_level' in request.data:
                    MAPS[i]['zoom_level'] = request.data['zoom_level']
                
                # Update the last_updated timestamp
                MAPS[i]['last_updated'] = datetime.now().isoformat()
                
                return Response(MAPS[i])
        
        # If no map is found, return 404
        return Response({"error": "Map not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        # Find the map with the given ID
        for i, map_data in enumerate(MAPS):
            if map_data['map_id'] == pk:
                # Remove the map from the list
                removed_map = MAPS.pop(i)
                return Response(status=status.HTTP_204_NO_CONTENT)
        
        # If no map is found, return 404
        return Response({"error": "Map not found"}, status=status.HTTP_404_NOT_FOUND)