from django.shortcuts import render
from django.urls import path


def sales(request):
    return render(request, "Sales/sales.html")

def view_sales(request):
    return render(request, "Sales/view_sales.html")


sales_templates = [
    path('sales/', sales, name='sales'),
    path('view_sales/', view_sales, name='view_sales')
]
