from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse
from django.contrib import messages
# from .forms import CustomersForm
from .models import Customers


##################################### Add & details Customer Functions ##########################################
def index(request):
    return render(request, "index.html")

def customers(request):
    # form_class = CustomersForm
    # form = CustomersForm(request.POST, request.FILES or None)
    if request.method == 'POST':
        # if form.is_valid():
        customer_name=request.POST.get('customer_name')
        customer_rank=request.POST.get('customer_rank')
        customer_id=request.POST.get('customer_id')
        customer_file=request.POST.get['customer_file']
        # form=CustomersForm(customer_name=customer_name, customer_rank=customer_rank, customer_id=customer_id, customer_file=customer_file)
        # form.save()
        messages.success(request, 'Customer added successfully')
        return redirect('Customers:customer_details')
        # else:
        #     print(form.errors)
        #     messages.error(request, 'Error adding customer')
    else:
        data = Customers.objects.all()
        return render(request, "Customers/customers.html", {'data': data})

def customer_details(request):
    return render(request, "Customers/customer_details.html")



index_template = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('customers/', customers, name='customers'),
    path('customer_details/', customer_details, name='customer_details')
]