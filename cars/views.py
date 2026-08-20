from django.shortcuts import render, get_object_or_404
from .filters import CarsFilter
from .models import Car


def car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car_detail.html', {'car': car})


def cars(request):
    f = CarsFilter(request.GET, queryset=Car.objects.all())
    return render(request, 'cars.html', {'filter': f})