from django.urls import path
from . import views

urlpatterns = [
    path('', views.cars, name='cars'),
    path('<int:car_id>', views.car, name='car_detail'),
    path('create/', views.create_car, name='car_create'),
    path('<int:car_id>/edit/', views.edit_car, name='car_edit'),
    path('<int:car_id>/delete/', views.delete_car, name='delete_car'),
    path('<int:car_id>/toggle_car/', views.toggle_car, name='toggle_car'),
    path('favorites/', views.favorites, name='favorites'),
    path('<int:car_id>/favorite/', views.favorite_car, name='favorite_car'),
]