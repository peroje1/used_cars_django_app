from django.test import TestCase
from django.urls import reverse
from listings.models import Car
from listings.forms import CarForm

class CarModelTest(TestCase):
    def setUp(self):
        self.car = Car.objects.create(
            brand="Toyota",
            model="Corolla",
            year=2015,
            price=8000,
            mileage=120000,
            city="Belgrade"
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "Toyota Corolla (2015)")

class CarViewsTest(TestCase):
    def setUp(self):
        self.car = Car.objects.create(
            brand="BMW",
            model="3 Series",
            year=2018,
            price=15000,
            mileage=70000,
            city="Novi Sad"
        )

    def test_car_list_view(self):
        response = self.client.get(reverse('car_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")

    def test_car_detail_view(self):
        response = self.client.get(reverse('car_detail', args=[self.car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3 Series")

class CarFormTest(TestCase):
    def test_valid_car_form(self):
        data = {
            'brand': 'Audi',
            'model': 'A4',
            'year': 2020,
            'price': 18000,
            'mileage': 30000,
            'city': 'Niš',
            'description': 'Well maintained',
        }
        form = CarForm(data=data)
        print("Errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_car_form(self):
        form = CarForm(data={})
        self.assertFalse(form.is_valid())
from django.test import TestCase

# Create your tests here.
