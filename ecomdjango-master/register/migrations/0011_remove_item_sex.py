# Generated by Django 3.0.2 on 2020-01-16 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0010_auto_20200116_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='sex',
        ),
    ]
