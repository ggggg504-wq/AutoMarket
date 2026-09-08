from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .filters import CarsFilter
from .forms import CarForm
from .models import Car, Favorite
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

def car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    is_favorite = (
        request.user.is_authenticated
        and Favorite.objects.filter(
            user=request.user,
            car=car
        ).exists()
    )

    return render(
        request,
        'car_detail.html',
        {
            'car': car,
            'is_favorite': is_favorite,
        }
    )


def cars(request):
    qs_filter = CarsFilter(
        request.GET,
        queryset=Car.objects.filter(
            is_active=True
        ).select_related('brand')
    )

    car_list = qs_filter.qs
    paginator = Paginator(car_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    params = request.GET.copy()
    params.pop('page', None)

    return render(
        request,
        'cars.html',
        {
            'filter': qs_filter,
            'params': params.urlencode(),
            'page_obj': page_obj
        }
    )

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

@login_required
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

@login_required
@require_POST
def delete_car(request, car_id):
    car = get_object_or_404(
        Car,
        id=car_id,
        owner=request.user
    )

    car.delete()
    return redirect('profile')

@login_required
@require_POST
def toggle_car(request, car_id):
    car = get_object_or_404(
        Car,
        id=car_id,
        owner=request.user
    )

    car.is_active = not car.is_active
    car.save()
    return redirect('profile')

@login_required
@require_POST
def favorite_car(request, car_id):
    car = get_object_or_404(
        Car,
        id=car_id,
        is_active=True
    )

    favorite = Favorite.objects.filter(
        user=request.user,
        car=car
    ).first()

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(
            car=car,
            user=request.user,
        )

    return redirect('favorites')

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related(
        'car',
        'car__brand'
    )

    paginator = Paginator(favorites, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'favorites.html', {'favorites': page_obj})