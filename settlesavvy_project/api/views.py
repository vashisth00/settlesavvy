# api/views.py

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Sum, Case, When, Value, FloatField

from accounts.models import User, RealtorProfile
from maps.models import Maps, Geographies, MapGeos, PointOfInterest
from factors.models import Factors, GeoFactors, MapFactors, MapFactorGeos
from .serializers import (
    UserSerializer, RealtorProfileSerializer,
    MapSerializer, GeographySerializer, MapGeoSerializer,
    FactorSerializer, GeoFactorSerializer, MapFactorSerializer, 
    MapFactorGeoSerializer, PointOfInterestSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class RealtorProfileViewSet(viewsets.ModelViewSet):
    queryset = RealtorProfile.objects.all()
    serializer_class = RealtorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['agency_name', 'service_areas']
    filterset_fields = ['user__is_active']
    

class MapViewSet(viewsets.ModelViewSet):
    queryset = Maps.objects.all()
    serializer_class = MapSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Maps.objects.all()
        return Maps.objects.filter(created_by=user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def factor_scores(self, request, pk=None):
        """Get aggregated scores for all neighborhoods in this map"""
        map_obj = self.get_object()
        
        # Get all map factors and their weights
        map_factors = MapFactors.objects.filter(map=map_obj, is_active=True)
        
        # Get all map geos (neighborhoods)
        map_geos = MapGeos.objects.filter(map=map_obj)
        
        # For each neighborhood, calculate its aggregate score
        results = []
        for map_geo in map_geos:
            geo_scores = MapFactorGeos.objects.filter(
                map_geo=map_geo,
                map_factor__in=map_factors,
                is_filtered_out=False
            )
            
            # Sum weighted scores
            if geo_scores.exists():
                total_weight = sum(mf.weight for mf in map_factors)
                weighted_score = sum(
                    score.aggregate_score * score.map_factor.weight 
                    for score in geo_scores
                ) / total_weight if total_weight > 0 else 0
                
                results.append({
                    'geo_id': map_geo.geo.geo_id,
                    'name': map_geo.name,
                    'score': weighted_score,
                    'geometry': map_geo.geo.geometry,
                    'is_filtered': False
                })
            else:
                # Neighborhood is filtered out
                results.append({
                    'geo_id': map_geo.geo.geo_id,
                    'name': map_geo.name, 
                    'score': 0,
                    'geometry': map_geo.geo.geometry,
                    'is_filtered': True
                })
                
        return Response(results)


class GeographyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Geographies.objects.all()
    serializer_class = GeographySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'geo_id', 'geo_type']
    
    @action(detail=False, methods=['get'])
    def by_location(self, request):
        """Get geographies near a specific location"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        
        if not lat or not lng:
            return Response(
                {"error": "Latitude and longitude are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            point = Point(float(lng), float(lat), srid=4326)
            geographies = Geographies.objects.filter(geometry__contains=point)
            serializer = self.get_serializer(geographies, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class MapGeoViewSet(viewsets.ModelViewSet):
    queryset = MapGeos.objects.all()
    serializer_class = MapGeoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['map']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MapGeos.objects.all()
        return MapGeos.objects.filter(map__created_by=user)


class FactorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Factors.objects.filter(is_active=True)
    serializer_class = FactorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description', 'category']
    filterset_fields = ['category', 'is_active']


class MapFactorViewSet(viewsets.ModelViewSet):
    queryset = MapFactors.objects.all()
    serializer_class = MapFactorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['map', 'factor', 'is_active']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MapFactors.objects.all()
        return MapFactors.objects.filter(map__created_by=user)
    
    @action(detail=True, methods=['post'])
    def calculate_scores(self, request, pk=None):
        """Calculate scores for all neighborhoods based on this factor"""
        map_factor = self.get_object()
        
        # Get all neighborhoods in this map
        map_geos = MapGeos.objects.filter(map=map_factor.map)
        
        # For each neighborhood, calculate score based on strategy
        for map_geo in map_geos:
            try:
                # Get the raw value for this factor in this geography
                geo_factor = GeoFactors.objects.get(
                    factor=map_factor.factor,
                    geo=map_geo.geo
                )
                
                # Calculate score based on strategy
                raw_value = geo_factor.value
                score = 0
                is_filtered = False
                
                # Apply scoring strategy
                if map_factor.scoring_strategy == 'higher_better':
                    # Normalize to 0-100 scale
                    if map_factor.score_tipping_2 and map_factor.score_tipping_1:
                        if raw_value >= map_factor.score_tipping_2:
                            score = 100
                        elif raw_value <= map_factor.score_tipping_1:
                            score = 0
                        else:
                            range_size = map_factor.score_tipping_2 - map_factor.score_tipping_1
                            if range_size > 0:
                                score = ((raw_value - map_factor.score_tipping_1) / range_size) * 100
                            else:
                                score = 50
                    else:
                        # Default normalization
                        score = min(raw_value * 10, 100)  # Basic scaling
                
                elif map_factor.scoring_strategy == 'lower_better':
                    # Normalize to 0-100 scale, inverting so lower is better
                    if map_factor.score_tipping_2 and map_factor.score_tipping_1:
                        if raw_value <= map_factor.score_tipping_1:
                            score = 100
                        elif raw_value >= map_factor.score_tipping_2:
                            score = 0
                        else:
                            range_size = map_factor.score_tipping_2 - map_factor.score_tipping_1
                            if range_size > 0:
                                score = 100 - ((raw_value - map_factor.score_tipping_1) / range_size) * 100
                            else:
                                score = 50
                    else:
                        # Default normalization
                        score = max(100 - (raw_value * 10), 0)  # Basic scaling
                
                # Apply filter strategy
                if map_factor.filter_strategy == 'above_threshold' and map_factor.filter_tipping_1:
                    is_filtered = raw_value < map_factor.filter_tipping_1
                
                elif map_factor.filter_strategy == 'below_threshold' and map_factor.filter_tipping_1:
                    is_filtered = raw_value > map_factor.filter_tipping_1
                
                elif map_factor.filter_strategy == 'between_thresholds' and map_factor.filter_tipping_1 and map_factor.filter_tipping_2:
                    is_filtered = raw_value < map_factor.filter_tipping_1 or raw_value > map_factor.filter_tipping_2
                
                elif map_factor.filter_strategy == 'outside_thresholds' and map_factor.filter_tipping_1 and map_factor.filter_tipping_2:
                    is_filtered = map_factor.filter_tipping_1 <= raw_value <= map_factor.filter_tipping_2
                
                # Save the score
                MapFactorGeos.objects.update_or_create(
                    geo_factor=geo_factor,
                    map_factor=map_factor,
                    map_geo=map_geo,
                    defaults={
                        'aggregate_score': score,
                        'raw_value': raw_value,
                        'is_filtered_out': is_filtered
                    }
                )
                
            except GeoFactors.DoesNotExist:
                # No data for this factor in this geography
                pass
        
        return Response({"status": "Scores calculated successfully"})


class PointOfInterestViewSet(viewsets.ModelViewSet):
    queryset = PointOfInterest.objects.all()
    serializer_class = PointOfInterestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['map', 'poi_type']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PointOfInterest.objects.all()
        return PointOfInterest.objects.filter(map__created_by=user)
    
    def perform_create(self, serializer):
        """Create a new point of interest"""
        lat = self.request.data.get('latitude')
        lng = self.request.data.get('longitude')
        
        if lat and lng:
            point = Point(float(lng), float(lat), srid=4326)
            serializer.save(location=point)
        else:
            return Response(
                {"error": "Latitude and longitude are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )