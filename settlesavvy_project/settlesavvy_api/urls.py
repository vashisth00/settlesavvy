# settlesavvy_api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from . import views

router = DefaultRouter()
# Register your viewsets with the router
router.register(r'maps', views.MapViewSet)
router.register(r'geographies', views.GeographyViewSet)
router.register(r'factors', views.FactorViewSet)
router.register(r'map-factors', views.MapFactorViewSet)

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', views.login_view, name='api_token_auth'),
    path('auth/register/', views.register_view, name='api_register'),
    
    # Debug endpoint
    path('debug/create-map/', views.debug_create_map, name='debug_create_map'),
    
    # Include router URLs
    path('', include(router.urls)),
    
    # API documentation endpoints
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Default authentication views
    path('auth/', include('rest_framework.urls')),
]