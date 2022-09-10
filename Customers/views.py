from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.http import HttpResponseRedirect
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
        if request.POST.get('Save'):
            try:
                Customers(customer_name=request.POST.get('customer_name'),
                          customer_rank=request.POST.get('customer_rank'),
                          customer_id=request.POST.get('customer_id'),
                          customer_file=request.FILES.get('customer_file')).save()

                messages.success(request, 'Customer Added Successful')
                return HttpResponseRedirect(reverse('Customers:customers'))
            except Exception as e:  # Exception as e:
                messages.error(request, 'Customer Added Failed')
                return HttpResponseRedirect(reverse('Customers:customers'))
    else:
        return render(request, 'Customers/customers.html', {'customers': Customers.objects.all().order_by("-id")})
        

def customer_details(request):
    return render(request, "Customers/customer_details.html", {'customers': Customers.objects.all().order_by("-id")})



index_template = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('customers/', customers, name='customers'),
    path('customer_details/', customer_details, name='customer_details')
]