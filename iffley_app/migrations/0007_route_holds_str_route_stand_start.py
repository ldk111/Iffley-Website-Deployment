# Generated by Django 4.2.2 on 2023-07-08 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iffley_app', '0006_route_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='holds_str',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='route',
            name='stand_start',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
