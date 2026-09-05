from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .filters import CarsFilter
from .forms import CarForm
from .models import Car
from django.core.paginator import Paginator

def car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car_detail.html', {'car': car})


def cars(request):
    qs_filter = CarsFilter(
        request.GET,
        queryset=Car.objects.filter(is_active=True)
    )

    car_list = qs_filter.qs
    paginator = Paginator(car_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    params = request.GET.copy()
    params.pop('page', None)
    return render(request, 'cars.html', {'filter': qs_filter, 'params': params.urlencode(),'page_obj': page_obj})

@login_required
def create_car(request):
    if request.method == 'GET':
        form = CarForm()
        return render(request, 'car_form.html', {'form': form})

    elif request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('cars')
        else:
            return render(request, 'car_form.html', {'form': form})

def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)

    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)

        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, 'car_form.html', {'form': form})

    else:
        form = CarForm(instance=car)
        return render(request, 'car_form.html', {'form': form})

def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)

    if request.method == 'POST':
        car.delete()
        return redirect('profile')

def toggle_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)
    if request.method == 'POST':
        car.is_active = not car.is_active
        car.save()
        return redirect('profile')

