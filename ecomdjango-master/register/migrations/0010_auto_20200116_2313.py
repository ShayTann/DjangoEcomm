# Generated by Django 3.0.2 on 2020-01-16 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0009_auto_20200114_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='subcategory',
            field=models.CharField(blank=True, choices=[('Shirt', 'Shirt'), ('Shoes', 'Shoes'), ('Jacket', 'Jacket'), ('Jeans', 'Jeans'), ('Hoodies', 'Hoodies'), ('Accesories', 'Accesories')], max_length=20, null=True),
        ),
    ]
