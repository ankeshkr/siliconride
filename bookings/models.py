from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings  # Import settings to use AUTH_USER_MODEL

class PickupPoint(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DestinationPoint(models.Model):
    name = models.CharField(max_length=100)
    origin = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, related_name='destinations')

    def __str__(self):
        return f"{self.name} (from {self.origin.name})"

class Traveller(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField()
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, related_name='travellers', default=1)
    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    origin = models.ForeignKey(PickupPoint, on_delete=models.CASCADE)
    destination = models.ForeignKey(DestinationPoint, on_delete=models.CASCADE)
    traveller = models.ForeignKey(Traveller, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Seat {self.seat_number} in {self.traveller.name}"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        extra_fields.setdefault('is_active', True)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Set a default value for 'age' during superuser creation
        if 'age' not in extra_fields:
            extra_fields['age'] = 0

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=10, unique=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    age = models.PositiveIntegerField()  # Required for regular users

    objects = CustomUserManager()

    def __str__(self):
        return self.name