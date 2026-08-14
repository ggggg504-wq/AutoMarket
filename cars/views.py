from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import SearchForm
from .models import Car


def car(request, car_id):
    car = Car.objects.get(id=car_id)
    return render(request, 'car_detail.html', {'car': car})


def cars(request):
    if request.method == "GET":
        form = SearchForm(request.GET)

        if form.is_valid():
            if form.cleaned_data['search'] == '':
                cars = Car.objects.all()
            else:
                cars = Car.objects.filter(
                    Q(brand__name__icontains=form.cleaned_data['search']) |
                    Q(model__icontains=form.cleaned_data['search']) |
                    Q(description__icontains=form.cleaned_data['search'])
                )
        else:
            cars = Car.objects.all()

        return render(request, 'cars.html', {'cars': cars})

    else:
        return HttpResponseRedirect('/cars')