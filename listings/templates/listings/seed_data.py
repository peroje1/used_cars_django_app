import os
import django
import random
from pathlib import Path

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Adjust if needed
django.setup()

from listings.models import Car

# Wipe existing cars
Car.objects.all().delete()

# Brand → Valid Models
brand_model_map = {
    "Toyota": ["Corolla", "Camry", "Rav4", "Yaris"],
    "BMW": ["320i", "X5", "X3", "M3"],
    "Volkswagen": ["Golf", "Passat", "Tiguan", "Polo"],
    "Ford": ["Focus", "Fiesta", "Mondeo", "Kuga"],
    "Audi": ["A3", "A4", "A6", "Q5"],
    "Mercedes": ["C-Class", "E-Class", "GLA", "GLC"],
    "Hyundai": ["Elantra", "Tucson", "i30", "Santa Fe"],
}

# Logo mapping (place logo files here: media/car_images/logos/)
brand_logos = {
    "Toyota": "logos/toyota.png",
    "BMW": "logos/bmw.png",
    "Volkswagen": "logos/volkswagen.png",
    "Ford": "logos/ford.png",
    "Audi": "logos/audi.png",
    "Mercedes": "logos/mercedes.png",
    "Hyundai": "logos/hyundai.png",
}

# Create logo folder if needed
media_root = Path("media/car_images/logos")
media_root.mkdir(parents=True, exist_ok=True)

cities = ["Belgrade", "Novi Sad", "Niš", "Kragujevac", "Subotica"]

conditions = ["excellent", "very good", "good", "fair", "like new"]
extras = [
    "Includes full service history.",
    "Winter tires included.",
    "Recently cleaned interior.",
    "No accident history.",
    "Smooth ride and low fuel consumption.",
    "One-owner vehicle.",
    "Battery and brakes recently replaced."
]

for i in range(1000):
    brand = random.choice(list(brand_model_map.keys()))
    model = random.choice(brand_model_map[brand])
    year = random.randint(1995, 2023)
    price = random.randint(1000, 30000)
    mileage = random.randint(5000, 300000)
    city = random.choice(cities)
    condition = random.choice(conditions)
    extra = random.choice(extras)
    description = f"Car is in {condition} condition. {extra}"

    logo_path = brand_logos.get(brand, "logos/default.png")

    car = Car(
        brand=brand,
        model=model,
        year=year,
        price=price,
        mileage=mileage,
        city=city,
        description=description,
        image=f"car_images/{logo_path}"  # assign image path before saving
    )

    car.save()

    if (i + 1) % 100 == 0:
        print(f"{i + 1} cars created")

print("All cars are created")
