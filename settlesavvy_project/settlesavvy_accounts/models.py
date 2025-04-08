# settlesavvy_accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Extended user model to include additional fields"""
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_realtor = models.BooleanField(default=False)
    
    # Add fields for preference storage
    preferred_city = models.CharField(max_length=100, blank=True, null=True)
    preferred_state = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.username

class RealtorProfile(models.Model):
    """Profile for realtors"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='realtor_profile')
    license_number = models.CharField(max_length=50)
    agency_name = models.CharField(max_length=255)
    service_areas = models.TextField()  # List of zip codes or areas served
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.agency_name}"