from django.db import models


class Customers(models.Model):
    customer_name = models.CharField(max_length=25)
    customer_rank = models.CharField(max_length=20)
    customer_id = models.CharField(max_length=10)
    customer_file = models.FileField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return self.customer_name
