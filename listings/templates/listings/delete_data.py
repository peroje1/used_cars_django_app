import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # replace myproject with your project name
django.setup()

from listings.models import Car

Car.objects.filter(model='Unknown').delete()

Car.objects.filter(brand='Other').delete()
