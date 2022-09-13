from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
# from .forms import CustomersForm
from .models import Customers
import pandas as pd
from django.core.files.storage import FileSystemStorage


def long_process(df):
    try:
        cols=['Customer Name','Customer Rank','Customer ID']
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
                          customer_file=request.FILES.get('customer_file')).save()
            elif request.POST.get('customer_file_submit'):
                # print("customer_file_submit")
                csv= request.FILES['customer_file']
                if not csv.name.split('.')[1] in ['csv', 'xlsx', 'xls']:
                    messages.error(request, 'This is not a correct formate file')
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
                        long_process(df)
                    elif csv.name.split('.')[-1] in ['xlsx','XLSX','xls','XLS']:
                        print("excel")
                        df = pd.read_excel("."+excel_file)
                        long_process(df)
                    else:
                        raise Exception("File not found") 
                    print('asdfadsf',df.shape)

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