from django.shortcuts import render
from django.urls import path

##################################### Add & details Customer Functions ##########################################
def index(request):
    return render(request, "index.html")

def customers(request):
    return render(request, "Customers/customers.html")

def customer_details(request):
    return render(request, "Customers/customer_details.html")



index_template = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('customers/', customers, name='customers'),
    path('customer_details/', customer_details, name='customer_details')
]