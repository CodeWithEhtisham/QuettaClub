# Generated by Django 4.0.3 on 2022-10-05 11:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0026_alter_dummytable_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dummytable',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
