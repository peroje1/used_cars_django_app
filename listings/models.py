from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Car(models.Model):
    BRAND_CHOICES = [
        ('Toyota', 'Toyota'),
        ('BMW', 'BMW'),
        ('Volkswagen', 'Volkswagen'),
        ('Ford', 'Ford'),
        ('Audi', 'Audi'),
        ('Mercedes', 'Mercedes'),
        ('Hyundai', 'Hyundai'),
        ('Other', 'Other'),
    ]

    CITY_CHOICES = [
        ('Belgrade', 'Belgrade'),
        ('Novi Sad', 'Novi Sad'),
        ('Niš', 'Niš'),
        ('Kragujevac', 'Kragujevac'),
        ('Subotica', 'Subotica'),
        ('Other', 'Other'),
    ]

    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField(help_text="Enter in kilometers")
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars', null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
