from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Car

@receiver(post_save, sender=Car)
def resize_car_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        try:
            img = Image.open(image_path)
            img = img.convert("RGB")

            max_size = (400, 300)
            img.thumbnail(max_size, Image.ANTIALIAS)
            img.save(image_path)
        except Exception as e:
            print(f"Image resize failed: {e}")
