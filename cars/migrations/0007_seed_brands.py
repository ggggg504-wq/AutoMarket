from django.db import migrations
from django.utils.text import slugify


def add_brands(apps, schema_editor):
    Brand = apps.get_model('cars', 'Brand')

    brands = [
        'BMW',
        'Toyota',
        'Audi',
        'Mercedes-Benz',
        'Volkswagen',
        'Honda',
        'Nissan',
        'Mazda',
        'Lexus',
        'Hyundai',
        'Kia',
        'Ford',
        'Chevrolet',
        'Renault',
        'Peugeot',
        'Skoda',
        'Subaru',
        'Volvo',
        'Porsche',
        'Tesla',
    ]

    for name in brands:
        brand, created = Brand.objects.get_or_create(
            name=name,
            defaults={
                'slug': slugify(name)
            }
        )

        if not brand.slug:
            brand.slug = slugify(name)
            brand.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_alter_car_engine'),
    ]

    operations = [
        migrations.RunPython(
            add_brands,
            reverse_code=migrations.RunPython.noop
        ),
    ]