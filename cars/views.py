from django.shortcuts import render, get_object_or_404
from .filters import CarsFilter
from .models import Car
from django.core.paginator import Paginator

def car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car_detail.html', {'car': car})


def cars(request):
    qs_filter = CarsFilter(request.GET, queryset=Car.objects.all())
    car_list = qs_filter.qs
    paginator = Paginator(car_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    params = request.GET.copy()
    params.pop('page', None)
    return render(request, 'cars.html', {'filter': qs_filter, 'params': params.urlencode(),'page_obj': page_obj})