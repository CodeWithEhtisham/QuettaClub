from django.db import models
from Customers.models import Customers

class Sales(models.Model):
    bill_no = models.CharField(max_length=50, null=False, blank=False)
    PoS_no = models.CharField(max_length=50, null=False, blank=False)
    month = models.CharField(max_length=50, null=False, blank=False)
    date = models.CharField(max_length=255,null=False, blank=False)
    address = models.CharField(max_length=50, null=False, blank=False)
    account_of = models.CharField(max_length=50, null=False, blank=False)
    amount = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True)
    net_amount = models.PositiveIntegerField()
    remarks = models.CharField(max_length=50, null=True, blank=True)    
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True, blank=True)


class Bill(models.Model):
    STATUS = (
        ('paid', 'Paid'),
        ('complementery', 'Complementery'),
        ('cancel', 'Cancel')
    )
    status = models.CharField(max_length=50, choices=STATUS, null=True, blank=True)
    rv_no = models.CharField(max_length=50) # only paid modal will have this field
    date = models.DateField() # all modal will have this field
    amount = models.PositiveIntegerField() # paid and complete modal will have this field
    bill_remarks = models.CharField(max_length=50, null=True, blank=True) # only complete modal will have this field
    reason = models.CharField(max_length=50, null=True, blank=True) # only cancel modal will have this field
    sale_id = models.ForeignKey(Sales, on_delete=models.CASCADE)


