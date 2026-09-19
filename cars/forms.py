from datetime import date

from django import forms

from .models import Car


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

    def clean_year(self):
        year = self.cleaned_data['year']
        current_year = date.today().year

        if year < 1950:
            raise forms.ValidationError(
                'Год выпуска не может быть раньше 1950.'
            )

        if year > current_year:
            raise forms.ValidationError(
                'Введите корректный год выпуска.'
            )

        return year

    def clean_mileage(self):
        mileage = self.cleaned_data['mileage']

        if mileage > 2_000_000:
            raise forms.ValidationError(
                'Укажите реальный пробег автомобиля.'
            )

        return mileage

    def clean_price(self):
        price = self.cleaned_data['price']

        if price <= 0:
            raise forms.ValidationError(
                'Цена должна быть больше 0.'
            )

        return price

    def clean_engine(self):
        engine = self.cleaned_data['engine']

        if engine < 0:
            raise forms.ValidationError(
                'Объём двигателя не может быть отрицательным.'
            )

        if engine > 15:
            raise forms.ValidationError(
                'Укажите корректный объём двигателя.'
            )

        return engine

    def clean(self):
        cleaned_data = super().clean()

        fuel = cleaned_data.get('fuel')
        engine = cleaned_data.get('engine')

        if (
            fuel
            and fuel != 'electric'
            and engine is not None
            and engine == 0
        ):
            self.add_error(
                'engine',
                'Для автомобиля с ДВС объём двигателя должен быть больше 0.'
            )

        return cleaned_data