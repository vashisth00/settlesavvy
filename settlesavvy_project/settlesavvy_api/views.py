# settlesavvy_api/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import Point
import json

from settlesavvy_accounts.models import User
from settlesavvy_core.models import Maps, Geographies, MapGeos, Factors, GeoFactors, MapFactors, MapFactorGeos
from .serializers import (
    MapSerializer, GeographySerializer, MapGeoSerializer, 
    FactorSerializer, GeoFactorSerializer, MapFactorSerializer,
    MapFactorGeoSerializer, NeighborhoodScoreSerializer
)

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def debug_create_map(request):
    """
    Debug view for map creation
    """
    try:
        # Extract data from request
        data = request.data
        name = data.get('name')
        latitude = float(data.get('latitude', 0))
        longitude = float(data.get('longitude', 0))
        zoom_level = float(data.get('zoom_level', 10))
        
        # Debug output
        print(f"Received data: {json.dumps(data, indent=2)}")
        print(f"Name: {name}")
        print(f"Lat: {latitude}, Lon: {longitude}")
        print(f"Zoom: {zoom_level}")
        
        # Create Point object
        center_point = Point(longitude, latitude, srid=4326)
        print(f"Created Point: {center_point}")
        
        # Create map object directly
        map_obj = Maps.objects.create(
            name=name,
            center_point=center_point,
            zoom_level=zoom_level,
            created_by=request.user
        )
        
        # Return success
        return Response({
            'success': True,
            'map_id': str(map_obj.map_id),
            'name': map_obj.name,
            'created_stamp': map_obj.created_stamp,
            'center_point': {
                'type': 'Point',
                'coordinates': [longitude, latitude]
            },
            'zoom_level': map_obj.zoom_level
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        # Return error with details
        print(f"Error creating map: {str(e)}")
        return Response({
            'success': False,
            'error': str(e),
            'detail': "An error occurred while creating the map"
        }, status=status.HTTP_400_BAD_REQUEST)

# ViewSets for models
class MapViewSet(viewsets.ModelViewSet):
    """ViewSet for Maps model"""
    queryset = Maps.objects.all()
    serializer_class = MapSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return maps for the current user or all maps if the user is staff"""
        if self.request.user.is_staff:
            return Maps.objects.all().order_by('-created_stamp')
        return Maps.objects.filter(created_by=self.request.user).order_by('-created_stamp')
    
    def get_serializer_context(self):
        """Add request to serializer context"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=True, methods=['get'])
    def scores(self, request, pk=None):
        """Get neighborhood scores for a map"""
        map_obj = self.get_object()
        
        # Get all MapGeos for this map
        map_geos = MapGeos.objects.filter(map=map_obj)
        
        # Get all MapFactors for this map
        map_factors = MapFactors.objects.filter(map=map_obj)
        
        # For each MapGeo, get scores from MapFactorGeos
        results = []
        
        for map_geo in map_geos:
            geo = map_geo.geo
            
            # Get score data
            map_factor_geos = MapFactorGeos.objects.filter(map_geo=map_geo)
            
            # Calculate aggregate score for this neighborhood
            total_score = 0
            total_weight = 0
            is_filtered = False
            
            for map_factor in map_factors:
                try:
                    # Try to find a specific score for this factor
                    mfg = map_factor_geos.get(map_factor=map_factor)
                    
                    # Check if this geography is filtered out by this factor
                    if map_factor.filter_strategy != 'no_filter':
                        if (map_factor.filter_strategy == 'less_than' and 
                            mfg.aggregate_score < map_factor.filter_tipping_1):
                            is_filtered = True
                            break
                        elif (map_factor.filter_strategy == 'greater_than' and 
                              mfg.aggregate_score > map_factor.filter_tipping_1):
                            is_filtered = True
                            break
                        elif (map_factor.filter_strategy == 'between' and 
                              (mfg.aggregate_score < map_factor.filter_tipping_1 or 
                               mfg.aggregate_score > map_factor.filter_tipping_2)):
                            is_filtered = True
                            break
                    
                    # Add to weighted score
                    total_score += mfg.aggregate_score * map_factor.weight
                    total_weight += map_factor.weight
                    
                except MapFactorGeos.DoesNotExist:
                    # Skip if no score for this factor
                    continue
            
            # Calculate final score (0-100)
            final_score = 0
            if total_weight > 0:
                final_score = min(100, max(0, round((total_score / total_weight) * 100)))
            
            # Add geometry data
            results.append({
                'geo_id': geo.geo_id,
                'name': geo.name,
                'score': final_score,
                'is_filtered': is_filtered,
                'geometry': json.loads(geo.geometry.json)
            })
        
        # Serialize and return
        serializer = NeighborhoodScoreSerializer(results, many=True)
        return Response(serializer.data)

class GeographyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Geographies model - read only"""
    queryset = Geographies.objects.all()
    serializer_class = GeographySerializer
    permission_classes = [permissions.IsAuthenticated]

class FactorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Factors model - read only"""
    queryset = Factors.objects.all()
    serializer_class = FactorSerializer
    permission_classes = [permissions.IsAuthenticated]

class MapFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for MapFactors model"""
    queryset = MapFactors.objects.all()
    serializer_class = MapFactorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter by map_id if provided"""
        map_id = self.request.query_params.get('map_id')
        if map_id:
            return MapFactors.objects.filter(map__map_id=map_id)
        
        # Only show factors for maps the user has created
        if not self.request.user.is_staff:
            return MapFactors.objects.filter(map__created_by=self.request.user)
        
        return MapFactors.objects.all()