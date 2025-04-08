# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import (
    UserViewSet, RealtorProfileViewSet,
    MapViewSet, GeographyViewSet, MapGeoViewSet, 
    FactorViewSet, MapFactorViewSet, PointOfInterestViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'realtors', RealtorProfileViewSet)
router.register(r'maps', MapViewSet)
router.register(r'geographies', GeographyViewSet)
router.register(r'map-geos', MapGeoViewSet)
router.register(r'factors', FactorViewSet)
router.register(r'map-factors', MapFactorViewSet)
router.register(r'points-of-interest', PointOfInterestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # API documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Authentication
    path('auth/', include('rest_framework.urls')),
]