# Generated by Django 3.0.2 on 2020-01-17 13:24

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0019_auto_20200117_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='shipping_country',
            field=django_countries.fields.CountryField(default='Morocco', max_length=2),
        ),
    ]
