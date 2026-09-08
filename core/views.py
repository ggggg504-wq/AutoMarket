from django.shortcuts import render
from cars.models import Car

def home(request):
    cars = Car.objects.filter(is_active=True).order_by('-created_at')[:6]
    return render(request, 'home.html', {'cars': cars})

