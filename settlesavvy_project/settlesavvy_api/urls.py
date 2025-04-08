# settlesavvy_api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from . import views

router = DefaultRouter()
# Register the MapViewSet
router.register(r'maps', views.MapViewSet, basename='maps')

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', views.login_view, name='api_token_auth'),
    path('auth/register/', views.register_view, name='api_register'),
    
    # Include router URLs
    path('', include(router.urls)),
    
    # API documentation endpoints
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Default authentication views
    path('auth/', include('rest_framework.urls')),
]