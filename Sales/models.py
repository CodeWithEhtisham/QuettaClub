from email.policy import default
from enum import auto
from django.db import models
from Customers.models import Customers
from django.utils import timezone

class Sales(models.Model):

    bill_no = models.CharField(max_length=50)
    PoS_no = models.CharField(max_length=50, null=False, blank=False)
    month = models.CharField(max_length=50, null=False, blank=False)
    created_date = models.DateTimeField()
    created_on  = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=50, null=False, blank=False)
    account_of = models.CharField(max_length=50, null=False, blank=False)
    amount = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True)
    net_amount = models.PositiveIntegerField()
    remarks = models.CharField(max_length=50, null=True, blank=True)    
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True, blank=True)

    def datepublished(self):
        return self.created_date.strftime('%B %d %Y')



class Bill(models.Model):
    STATUS = (
        ('paid', 'Paid'),
        ('complementery', 'Complementery'),
        ('cancel', 'Cancel')
    )
    status = models.CharField(max_length=50, choices=STATUS, null=True, blank=True)
    rv_no = models.CharField(max_length=50, null=True) # only paid modal will have this field
    date = models.DateField() # all modal will have this field
    amount = models.PositiveIntegerField(default=0) # paid and complete modal will have this field
    bill_remarks = models.CharField(max_length=50, null=True, blank=True) # only complete modal will have this field
    reason = models.CharField(max_length=50, null=True, blank=True) # only cancel modal will have this field
    sale_id = models.ForeignKey(Sales, on_delete=models.CASCADE)


