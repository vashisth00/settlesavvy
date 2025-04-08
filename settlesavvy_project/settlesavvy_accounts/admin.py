# settlesavvy_accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, RealtorProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_realtor', 'is_staff')
    list_filter = ('is_realtor', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Settle Savvy Info', {'fields': ('phone', 'is_realtor', 'preferred_city', 'preferred_state')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Settle Savvy Info', {'fields': ('phone', 'is_realtor', 'preferred_city', 'preferred_state')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'preferred_city')

class RealtorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency_name', 'license_number', 'created_at')
    search_fields = ('user__username', 'user__email', 'agency_name', 'license_number')
    list_filter = ('created_at',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(RealtorProfile, RealtorProfileAdmin)