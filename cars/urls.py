from django.urls import path
from . import views

urlpatterns = [
    path('', views.cars, name='cars'),
    path('<int:car_id>', views.car, name='car_detail'),
    path('create/', views.create_car, name='car_create'),
]