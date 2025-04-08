# settlesavvy_api/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import Point
import json

from settlesavvy_accounts.models import User
# Instead of importing from settlesavvy_core, import directly from your djando core model

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

# Create a simple MapViewSet to respond to the API endpoint
class MapViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving maps.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        # Just return an empty list for now
        return Response([])
    
    def retrieve(self, request, pk=None):
        # Return a 404 if the map doesn't exist
        return Response({"error": "Map not found"}, status=status.HTTP_404_NOT_FOUND)