from django.db import models

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    transmission = models.CharField(max_length=30)
    fuel = models.CharField(max_length=30)
    mileage = models.PositiveIntegerField()
    city = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    engine = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return f'{self.brand} {self.model}'