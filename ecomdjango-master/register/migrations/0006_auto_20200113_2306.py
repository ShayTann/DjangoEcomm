# Generated by Django 3.0.2 on 2020-01-13 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_item_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='subcategory',
            field=models.CharField(blank=True, choices=[('Boy', 'Boy'), ('Girl', 'Girl'), ('Shoes', 'Shoes'), ('Jacket', 'Jacket'), ('Jeans', 'Jeans'), ('Hoodies', 'Hoodies'), ('Accesories', 'Accesories')], max_length=20, null=True),
        ),
    ]
