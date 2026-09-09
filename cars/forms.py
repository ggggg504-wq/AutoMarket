from django import forms
from cars.models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car

        fields = [
            'brand',
            'model',
            'year',
            'engine',
            'price',
            'transmission',
            'fuel',
            'mileage',
            'city',
            'description',
        ]

        labels = {
            'brand': 'Марка',
            'model': 'Модель',
            'year': 'Год выпуска',
            'engine': 'Объём двигателя',
            'price': 'Цена',
            'transmission': 'Коробка передач',
            'fuel': 'Топливо',
            'mileage': 'Пробег',
            'city': 'Город',
            'description': 'Описание',
        }

        widgets = {
            'brand': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'model': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'year': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'engine': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'price': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'transmission': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'fuel': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'mileage': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'city': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                }
            ),
        }