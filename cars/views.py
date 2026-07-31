from django.shortcuts import render
from .models import Car


def car(request, id):
    avto = Car.objects.get(id=id)
    return render(request, 'car_detail.html', {'avto': avto})

def cars(request):
    cars = Car.objects.all()
    return render(request, 'cars.html', {'cars': cars})