from dataclasses import field
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.contrib import messages
from .models import Sales
from Customers.models import Customers
import pandas as pd
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import SalesSerializer

def long_process(df):
    try:
        df.rename(columns=df.iloc[0], inplace = True)
        df.drop(df.index[0], inplace = True)
        print(df.columns)
        # rename the columns
        df.rename(columns={'Bill No': 'bill_no', 'POS NO': 'PoS_no', 'Month': 'month', 'Dated': 'date', 'Address': 'address', 'On Account Of': 'account_of', 'Amount': 'amount', 'Discount ': 'discount', 'Net Amount': 'net_amount', 'Remarks': 'remarks', 'Name': 'customer_name', 'Rank': 'customer_rank'}, inplace=True)
        df['month'] = pd.to_datetime(df['month'], format='%d-%m').dt.strftime('%d-%B')
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y').dt.strftime('%d-%m-%Y')

        df=df[['bill_no','PoS_no','month','date','address','account_of','amount','discount','net_amount','remarks','customer_name','customer_rank']]
        for index, row in df.iterrows():
            customer=Customers.objects.filter(customer_name=row['customer_name'],customer_rank=row['customer_rank']).first()
            Sales(bill_no=row['bill_no'],
                PoS_no=row['PoS_no'],
                month=row['month'],
                #   ['“Sept. 30, 2022” value has an invalid date format. It must be in YYYY-MM-DD format.']
                date=row['date'],
                address=row['address'],
                account_of=row['account_of'],
                amount=row['amount'],
                discount=row['discount'],
                net_amount=row['net_amount'],
                remarks=row['remarks'],
                customer_id=customer
                ).save()
        return True
    except Exception as e:
        print(e)
        return False
        

def sales(request):
    if request.method == 'POST':
        try:
            if request.POST.get('Save'):
                # print(request.POST.get('customer_name'))
                
                customer=Customers.objects.filter(customer_name=request.POST.get('customer_name'),customer_rank=request.POST.get('customer_rank')).first()
                # print(customer)
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
                      customer_id=customer
                      ).save()

                messages.success(request, 'Sales Added Successful')
                return HttpResponseRedirect(reverse("Sales:sales"))
            elif request.POST.get('sale_file_submit'):
                # print("customer_file_submit")
                csv= request.FILES['sale_file']
                if not csv.name.split('.')[1] in ['csv', 'xlsx', 'xls']:
                    messages.error(request, 'This is not a correct format file')
                else:
                    myfile = request.FILES["sale_file"]        
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name, myfile)
                    uploaded_file_url = fs.url(filename)
                    excel_file = uploaded_file_url
                    # print("."+excel_file)
                    # print(csv.name.split('.')[-1])
                    if csv.name.split('.')[-1] in ['csv','CSV']:
                        print("csv")
                        df = pd.read_csv("."+excel_file)
                        if long_process(df):
                            messages.success(request, 'Sales csv Added Successful')
                            return HttpResponseRedirect(reverse("Sales:sales"))
                    elif csv.name.split('.')[-1] in ['xlsx','XLSX','xls','XLS']:
                        print("excel")
                        df = pd.read_excel("."+excel_file)
                        if long_process(df):
                            messages.success(request, 'Sales excel Added Successful')
                            return HttpResponseRedirect(reverse("Sales:sales"))
                raise Exception("File not found") 
        except Exception as e:  # Exception as e:
                messages.error(request, 'Sales Added Failed',e)
                return HttpResponse("Please fill the required fields! Back to Sales page {}".format(e), status=400)

    else:            
        return render(request, "Sales/sales.html", {'customers': Customers.objects.all()})

def view_sales(request):
    return render(request, "Sales/view_sales.html",
                {'sales_data': Sales.objects.select_related('customer_id').order_by("-bill_no")})

def reports(request):
    return render(request, "Sales/reports.html",
                {'sales_data': Sales.objects.select_related('customer_id').order_by("-bill_no")})

@api_view(['GET'])
def SearchbyName(request):
    field = request.GET.get('field')
    value = request.GET.get('value')
    print(field,value)
    try:
        if field=='name':
            return Response(SalesSerializer(Sales.objects.select_related('customer_id').filter(customer_id__customer_name__icontains=value).order_by('-id'), many=True).data)
        elif field=='rank':
            return Response(SalesSerializer(Sales.objects.select_related('customer_id').filter(customer_id__customer_rank__icontains=value).order_by('-id'), many=True).data)
        elif field=='bill_no':
            return Response(SalesSerializer(Sales.objects.filter(bill_no__icontains=value).order_by('-id'), many=True).data)
        elif field=='Pos_no':
            return Response(SalesSerializer(Sales.objects.filter(PoS_no__icontains=value).order_by('-id'), many=True).data)
        elif field=='month':
            return Response(SalesSerializer(Sales.objects.filter(month__icontains=value).order_by('-id'), many=True).data)
        elif field=='account_of':
            return Response(SalesSerializer(Sales.objects.filter(account_of__icontains=value).order_by('-id'), many=True).data)
        elif field=='date':
            return Response(SalesSerializer(Sales.objects.filter(date__icontains=value).order_by('-id'), many=True).data)
        elif field=='address':
            return Response(SalesSerializer(Sales.objects.filter(address__icontains=value).order_by('-id'), many=True).data)
    except Exception as e:
        return Response({"message": "No data found {}".format(e)})


sales_templates = [
    path('sales/', sales, name='sales'),
    path('view_sales/', view_sales, name='view_sales'),
    path('api/SearchbyName/', SearchbyName, name='SearchbyName'),
    path('reports/', reports, name='reports'),
]
