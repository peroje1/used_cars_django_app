from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price', 'mileage', 'city')  # 👁 columns shown
    list_filter = ('brand', 'year', 'city')                                # 🔍 filters in sidebar
    search_fields = ('brand', 'model', 'description', 'city')              # 🔎 top search box
    ordering = ('-year',)                                                  # 🗂 sorted newest first
