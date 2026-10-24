from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import CarForm
from .models import Brand, Car, Favorite


class BrandModelTests(TestCase):

    def test_brand_slug_created_automatically(self):
        brand = Brand.objects.create(name='TestBrand')

        self.assertEqual(brand.slug, 'testbrand')

    def test_str(self):
        brand = Brand.objects.create(name='TestBrand')

        self.assertEqual(str(brand), 'TestBrand')

    def test_car_is_active_by_default(self):
        user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        brand = Brand.objects.create(name='TestBrand')

        car = Car.objects.create(
            brand=brand,
            owner=user,
            model='E34',
            year=1995,
            price=5000000,
            transmission='manual',
            fuel='petrol',
            mileage=200000,
            city='astana',
            engine=2.5
        )

        self.assertTrue(car.is_active)

    def test_car_str(self):
        user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        brand = Brand.objects.create(name='TestBrand')

        car = Car.objects.create(
            brand=brand,
            owner=user,
            model='E34',
            year=1995,
            price=5000000,
            transmission='manual',
            fuel='petrol',
            mileage=200000,
            city='astana',
            engine=2.5
        )

        self.assertEqual(str(car), 'TestBrand E34')

    def test_valid_car_form(self):
        brand = Brand.objects.create(name='TestBrand')

        data = {
            'brand': brand.id,
            'model': 'E34',
            'year': 1995,
            'price': 5000000,
            'transmission': 'manual',
            'fuel': 'petrol',
            'mileage': 200000,
            'city': 'astana',
            'engine': 2.5,
            'description': 'BMW'
        }

        form = CarForm(data=data)

        self.assertTrue(form.is_valid())

    def test_valid_car_form_year(self):
        brand = Brand.objects.create(name='TestBrand')

        data = {
            'brand': brand.id,
            'model': 'E34',
            'year': 1949,
            'price': 5000000,
            'transmission': 'manual',
            'fuel': 'petrol',
            'mileage': 200000,
            'city': 'astana',
            'engine': 2.5,
            'description': 'BMW'
        }

        form = CarForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn('year', form.errors)

    def test_valid_car_form_future_year(self):
        brand = Brand.objects.create(name='TestBrand')

        data = {
            'brand': brand.id,
            'model': 'E34',
            'year': 2100,
            'price': 5000000,
            'transmission': 'manual',
            'fuel': 'petrol',
            'mileage': 200000,
            'city': 'astana',
            'engine': 2.5,
            'description': 'BMW'
        }

        form = CarForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn('year', form.errors)

    def test_valid_car_form_price(self):
        brand = Brand.objects.create(name='TestBrand')

        data = {
            'brand': brand.id,
            'model': 'E34',
            'year': 1995,
            'price': 0,
            'transmission': 'manual',
            'fuel': 'petrol',
            'mileage': 200000,
            'city': 'astana',
            'engine': 2.5,
            'description': 'BMW'
        }

        form = CarForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_valid_car_form_engine(self):
        brand = Brand.objects.create(name='TestBrand')

        data = {
            'brand': brand.id,
            'model': 'E34',
            'year': 1995,
            'price': 500000,
            'transmission': 'manual',
            'fuel': 'petrol',
            'mileage': 200000,
            'city': 'astana',
            'engine': 0,
            'description': 'BMW'
        }

        form = CarForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn('engine', form.errors)

    def test_valid_car_form_electric(self):
        brand = Brand.objects.create(name='TestBrand')

        data = {
            'brand': brand.id,
            'model': 'E34',
            'year': 1995,
            'price': 500000,
            'transmission': 'manual',
            'fuel': 'electric',
            'mileage': 200000,
            'city': 'astana',
            'engine': 0,
            'description': 'BMW'
        }

        form = CarForm(data=data)

        self.assertTrue(form.is_valid())

    def test_cars_page_opens(self):
        url = reverse('cars')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_car_requires_login(self):
        url = reverse('car_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_other_user_cannot_edit_car(self):
        brand = Brand.objects.create(name='TestBrand')

        other_user = User.objects.create_user(
            username='test',
            password='12345'
        )

        owner = User.objects.create_user(
            username='owner',
            password='12345'
        )

        car = Car.objects.create(
            brand=brand,
            owner=owner,
            model='E34',
            year=1995,
            price=5000000,
            transmission='manual',
            fuel='petrol',
            mileage=200000,
            city='astana',
            engine=2.5
        )

        self.client.login(
            username='test',
            password='12345'
        )

        url = reverse('car_edit', args=[car.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_user_can_add_car_to_favorites(self):
        brand = Brand.objects.create(name='TestBrand')
        owner = User.objects.create_user(
            username='owner',
            password='12345'
        )

        other_user = User.objects.create_user(
            username='other',
            password='12345'
        )

        car = Car.objects.create(
            brand=brand,
            owner=owner,
            model='E34',
            year=1995,
            price=5000000,
            transmission='manual',
            fuel='petrol',
            mileage=200000,
            city='astana',
            engine=2.5
        )

        self.client.login(
            username='other',
            password='12345'
        )

        url = reverse('favorite_car', args=[car.id])
        response = self.client.post(url)

        self.assertTrue(
            Favorite.objects.filter(
                user=other_user,
                car=car
            ).exists()
        )