from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
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

@login_required
def profile(request):
    cars = Car.objects.filter(
        owner=request.user
    ).select_related('brand')
    return render(request, 'profile.html', {'cars': cars})