from django.shortcuts import render
from .models import Car


def car(request, id):
    avto = Car.objects.get(id=id)
    return render(request, 'car.html', {'avto': avto})