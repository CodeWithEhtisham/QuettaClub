# Generated by Django 4.1 on 2022-09-28 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Sales", "0010_remove_sales_date_sales_created_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sales",
            name="created_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
