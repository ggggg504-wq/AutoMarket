from django.db import models
from django.utils.text import slugify

class Brand(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('manual', 'МКПП'),
        ('automatic', 'АКПП'),
        ('cvt', 'Вариатор'),
        ('robot', 'Робот')
    ]

    FUEL_CHOICES = [
        ('petrol', 'Бензин'),
        ('gas', 'Газ'),
        ('diesel', 'Дизель'),
        ('hybrid', 'Гибрид'),
        ('electric', 'Электро'),
    ]

    CITY_CHOICES = [
        ('astana', 'Астана'),
        ('almaty', 'Алматы'),
        ('shymkent', 'Шымкент'),
        ('karaganda', 'Караганда'),
        ('aktobe', 'Актобе'),
        ('atyrau', 'Атырау'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES)
    mileage = models.PositiveIntegerField()
    city = models.CharField(max_length=30, choices=CITY_CHOICES)
    description = models.TextField(blank=True)
    engine = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.brand.name} {self.model}'