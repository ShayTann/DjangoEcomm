# Generated by Django 3.0.2 on 2020-01-17 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0018_auto_20200117_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
