from django.contrib import admin
from .models import Car, Brand

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'price', 'city', 'created_at']
    list_filter = ['brand','year', 'fuel', 'transmission', 'city']
    search_fields = ['model', 'description']
    date_hierarchy = 'created_at'