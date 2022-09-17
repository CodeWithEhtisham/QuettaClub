from dataclasses import field
from multiprocessing.sharedctypes import Value
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from Sales.models import Sales
# from .forms import CustomersForm
from .models import Customers
import pandas as pd
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CustomersSerializer


def long_process(df):
    try:
        df.rename(columns=df.iloc[0], inplace = True)
        df.drop(df.index[0], inplace = True)
        # rename columns
        df.rename(columns={'Name': 'customer_name', 'Rank': 'customer_rank', 'Ser No ': 'customer_id'}, inplace=True)
        print(df.columns)
        cols=['customer_name','customer_rank','customer_id']
        df=df[cols]
        df=df.to_dict('records')
        print(df)
        model_isntance = [Customers(**data) for data in df]
        obj=Customers.objects.bulk_create(model_isntance)
        print(obj)
        print("success")
        return True
    except Exception as e:
        print("failed",e)
        return False

##################################### Add & details Customer Functions ##########################################
def index(request):
    return render(request, "index.html")

def customers(request):
    if request.method == 'POST':
        try:
            if request.POST.get('Save'):
                Customers(customer_name=request.POST.get('customer_name'),
                          customer_rank=request.POST.get('customer_rank'),
                          customer_id=request.POST.get('customer_id'),
                            customer_address=request.POST.get('customer_address'),
                          customer_file=request.FILES.get('customer_file')).save()
                return HttpResponseRedirect(reverse('Customers:customers'))
            elif request.POST.get('customer_file_submit'):
                # print("customer_file_submit")
                csv= request.FILES['customer_file']
                if not csv.name.split('.')[1] in ['csv', 'xlsx', 'xls']:
                    messages.error(request, 'This is not a correct formate file')
                    return HttpResponseRedirect(reverse('Customers:customers'))
                else:
                    myfile = request.FILES["customer_file"]        
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name, myfile)
                    uploaded_file_url = fs.url(filename)
                    excel_file = uploaded_file_url
                    print("." + excel_file)
                    print(csv.name.split('.')[-1])
                    if csv.name.split('.')[-1] in ['csv','CSV']:
                        df = pd.read_csv("."+excel_file)
                        if long_process(df):
                            messages.success(request, 'csv added to database')
                            return HttpResponseRedirect(reverse('Customers:customers'))
                    elif csv.name.split('.')[-1] in ['xlsx','XLSX','xls','XLS']:
                        print("excel")
                        df = pd.read_excel("."+excel_file)
                        if long_process(df):
                            messages.success(request, 'excel added to database')
                            return HttpResponseRedirect(reverse('Customers:customers'))
                    
                    raise Exception("File not found") 
            # if request.POST.get('edit_customer'):
            #     return render(request, "Customers/customer_update.html", {'customer_data': Customers.objects.filter(id=request.POST.get("cid"))[0]})

        except Exception as e:  # Exception as e:
                messages.error(request, 'Customer Added Failed {}'.format(e))
                return HttpResponseRedirect(reverse('Customers:customers'))
    else:
        return render(request, 'Customers/customers.html', 
            {'customers': Customers.objects.all().order_by("-id")
            })


def customer_update(request):
    if request.method == 'POST':
        try:
            if request.POST.get('update_customer'):
                Customers.objects.filter(id=request.POST.get('cid')).update(
                    customer_name=request.POST.get('customer_name'),
                    customer_rank=request.POST.get('customer_rank'),
                    customer_id=request.POST.get('customer_id'),
                    customer_address=request.POST.get('customer_address'))
                    
                return HttpResponseRedirect(reverse('Customers:customers'))
        except Exception as e:
            messages.error(request, 'Customer Update Failed {}'.format(e))
            return HttpResponseRedirect(reverse('Customers:customers'))
    else:
        return render(request, "Customers/customer_update.html", 
        {'customer_data': Customers.objects.filter(id=request.GET.get("id")).first()})
        

def customer_details(request):
    print( Sales.objects.filter(customer_id__id=request.GET.get("id")).select_related('customer_id').order_by("-id"))
    return render(request, "Customers/customer_details.html", {'Sales_data': Sales.objects.filter(customer_id__id=request.GET.get("id")).select_related('customer_id').order_by("-id")})


@api_view(['GET'])
def SearchCustomer(request):
    field = request.GET.get('field')
    value = request.GET.get('value')

    try:
        if field == 'Name':
            return Response(CustomersSerializer(Customers.objects.filter(customer_name__icontains=value).order_by('-id'), many=True).data)
        elif field == 'Rank':
            return Response(CustomersSerializer(Customers.objects.filter(customer_rank__icontains=value).order_by('-id'), many=True).data)
        elif field == 'ID':
            return Response(CustomersSerializer(Customers.objects.filter(customer_id__icontains=value).order_by('-id'), many=True).data)
        # else:
        #     customers = Customers.objects.all()
    except Exception as e:
        return Response({"message": "No data found {}".format(e)})


index_template = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('customers/', customers, name='customers'),
    path('customer_details/', customer_details, name='customer_details'),
    path('api/SearchCustomer/', SearchCustomer, name='SearchCustomer'),
    path('customer_update/', customer_update, name='customer_update'),
]