# Generated by Django 3.0.2 on 2020-01-16 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0015_auto_20200116_2328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('numero', models.CharField(blank=True, max_length=50, null=True)),
                ('message', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
