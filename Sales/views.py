from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.contrib import messages
from .models import Sales
from Customers.models import Customers


def sales(request):
    if request.method == 'POST':
        if request.POST.get('Save'):
            try:
                Sales(bill_no=request.POST.get('bill_no'),
                      PoS_no=request.POST.get('PoS_no'),
                      month=request.POST.get('month'),
                      date=request.POST.get('date'),
                      address=request.POST.get('address'),
                      account_of=request.POST.get('account_of'),
                      amount=request.POST.get('amount'),
                      discount=request.POST.get('discount'),
                      net_amount=request.POST.get('net_amount'),
                      remarks=request.POST.get('remarks'),
                    #   customer_id=Customers.objects.filter(
                    #         customer_name=request.POST.get('customer_name'),
                    #         customer_rank=request.POST.get('customer_rank')).first()
                      ).save()

                messages.success(request, 'Sales Added Successful')
                return HttpResponseRedirect(reverse("Sales:sales"))
            except Exception as e:  # Exception as e:
                messages.error(request, 'Sales Added Failed')
                return HttpResponse("Please fill the required fields! Back to Sales page", status=400)

    else:            
        return render(request, "Sales/sales.html")

def view_sales(request):
    return render(request, "Sales/view_sales.html",
                  {'sales_data': Sales.objects.all().order_by("-id")})


sales_templates = [
    path('sales/', sales, name='sales'),
    path('view_sales/', view_sales, name='view_sales')
]
