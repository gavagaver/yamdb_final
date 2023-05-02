# Generated by Django 3.2 on 2023-01-29 14:56

import reviews.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, validators=[reviews.validator.validate_year], verbose_name='Год'),
        ),
    ]
