from django.contrib import admin
from .models import PickupPoint, DestinationPoint, Traveller, Booking, CustomUser  # Import models
from django.contrib.auth.admin import UserAdmin

# Register your models here
admin.site.register(PickupPoint)
admin.site.register(DestinationPoint)
admin.site.register(Traveller)
admin.site.register(Booking)

#admin.site.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'mobile')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
