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


class Bills(models.Model):
    rv_no = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    amount = models.PositiveIntegerField()
    bill_remarks = models.CharField(max_length=50, null=True, blank=True)
    reason = models.CharField(max_length=50, null=True, blank=True)
    sales_id = models.ForeignKey(Sales, on_delete=models.CASCADE, null=True, blank=True)
    

