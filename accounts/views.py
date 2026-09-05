from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login

from cars.models import Car


def register(request):
    if request.user.is_authenticated:
        return redirect('cars')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cars')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def profile(request):
    cars = Car.objects.filter(owner=request.user)
    return render(request, 'profile.html',{'cars': cars})