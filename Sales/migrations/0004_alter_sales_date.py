# Generated by Django 4.0.3 on 2022-09-13 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0003_sales_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='date',
            field=models.CharField(max_length=255),
        ),
    ]
