from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.contrib import messages
from grpc import Status
from .models import Sales, Bill
from Customers.models import Customers
import pandas as pd
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import SalesSerializer
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.db import models

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
                
                customer=Customers.objects.filter(customer_name=request.POST.get('customer_name'),
                    customer_rank=request.POST.get('customer_rank')).first()
                # print(customer)
                Sales.objects.filter(created_on__date=timezone.now()).create(
                                bill_no=request.POST.get('bill_no'),
                                PoS_no=request.POST.get('PoS_no'),
                                month=request.POST.get('month'),
                                created_date=request.POST.get('date'),
                                created_on=request.POST.get('created_on'),
                                address=request.POST.get('address'),
                                account_of=request.POST.get('account_of'),
                                amount=request.POST.get('amount'),
                                discount=request.POST.get('discount'),
                                net_amount=request.POST.get('net_amount'),
                                remarks=request.POST.get('remarks'),
                                customer_id=customer
                                )

                messages.success(request, 'Sales Added Successful')
                return HttpResponseRedirect(reverse("Sales:sales"))
            
            if request.POST.get('upload_bills'):
                Sales.objects.filter(created_on__date=timezone.now()).save()
                messages.success(request, 'Sales Added Successful')
                return HttpResponseRedirect(reverse("Sales:sales"))

            # if request.POST.get('delete_bills'):
            #     Sales.objects.filter(created_date__date=timezone.now()).delete()
            #     messages.success(request, 'Sales Deleted Successful')
            #     return HttpResponseRedirect(reverse("Sales:sales"))

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
        return render(request, "Sales/sales.html", {
            'customers': Customers.objects.all(),
            'sales': Sales.objects.all(),
            'today_sale': Sales.objects.filter(created_on__date=timezone.now()),
            })

def view_sales(request):
    if request.method == "POST":
        try:
            pass
        except Exception as e:
            pass
    else:
        return render(request, "Sales/view_sales.html",
                {'sales_data': Sales.objects.all().exclude(created_on__date=timezone.now()).select_related('customer_id').order_by("-bill_no"),
                'total_bills': Sales.objects.select_related('bill_no').count(),
                'total_amount': Sales.objects.aggregate(Sum('amount'))['amount__sum'],
                'total_discount': Sales.objects.aggregate(Sum('discount'))['discount__sum'],
                'total_net_amount': Sales.objects.aggregate(Sum('net_amount'))['net_amount__sum'],
                # 'total_paid': Sales.objects.aggregate(Sum('paid')['paid__sum']),
                # 'total_paid_bills': Sales.objects.aggregate(Sum('paid_bill'),
                # 'total_cancelled_bills': Sales.objects.aggregate(Sum('cancelled_bill'),
                # 'total_complement_bills': Sales.objects.aggregate(Sum('complement_bill')
                })

def update_sales(request):
    if request.method == "POST":
        try:
            if request.POST.get('update_bill'):
                customer=Customers.objects.filter(customer_name=request.POST.get('customer_name'),
                    customer_rank=request.POST.get('customer_rank')).first()

                Sales.objects.filter(id=request.POST.get('edit_id')).update(
                    bill_no=request.POST.get('bill_no'),
                    PoS_no=request.POST.get('PoS_no'),
                    month=request.POST.get('month'),
                    created_date=request.POST.get('date'),
                    address=request.POST.get('address'),
                    account_of=request.POST.get('account_of'),
                    amount=request.POST.get('amount'),
                    discount=request.POST.get('discount'),
                    net_amount=request.POST.get('net_amount'),
                    remarks=request.POST.get('remarks'),
                    customer_id=customer)
                
                return HttpResponseRedirect(reverse("Sales:view_sales"))
            if request.POST.get('cancel'):
                return HttpResponseRedirect(reverse("Sales:view_sales"))
        except Exception as e:
            messages.error(request, f'Sales Update Failed {e}')
            return HttpResponseRedirect(reverse("Sales:view_sales"))

    else:
        print("edit id ",request.POST.get('edit_id'))
        print(Sales.objects.filter(id=request.GET.get('edit_id')).select_related('customer_id').first())
        return render(request, "Sales/update_sales.html", {
                'sales_data': Sales.objects.filter(id=request.GET.get('id')).select_related('customer_id').first(),
                'customers': Customers.objects.all(),
            })


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


@api_view(['GET', 'POST'])
def sales_pay_bill(request):
    if request.method == "POST":
        id = request.POST.get('id')
        rv_no = request.POST.get('rv_no')
        paid_date = request.POST.get('paid_date')
        amount = request.POST.get('amount')
        remaining_amount = request.POST.get('remaining_amount')
        print("remaining amount ", remaining_amount)

        Bill.objects.create(rv_no=rv_no, date=paid_date, amount=amount, 
            status = "Paid", sale_id=Sales.objects.get(id=id))

        Sales.objects.filter(id=id).update(net_amount=remaining_amount)

        print("sale net amount ", Sales.objects.filter(id=id).first())
        return Response({"message": "Bill Paid Successfully"})

@api_view(['GET', 'POST'])
def sales_comp_bill(request):
    if request.method == "POST":
        id = request.POST.get('id')
        date = request.POST.get('comp_date')
        amount = request.POST.get('comp_amount')
        remarks = request.POST.get('comp_remarks')
        remaining_amount = request.POST.get('remaining_amount')

        Bill.objects.create(amount=amount, date=date, bill_remarks=remarks, 
            status="Complementery", sale_id=Sales.objects.get(id=id))

        Sales.objects.filter(id=id).update(net_amount=remaining_amount)
        return Response({"message": "Complement Bill Added Successfully"})

@api_view(['GET', 'POST'])
def sales_cancel_bill(request):

    if request.method == "POST":
        id = request.POST.get('id')
        date = request.POST.get('cancel_date')
        reason = request.POST.get('reason')

        Bill.objects.create(date=date, reason=reason,
           status='Cancel', sale_id=Sales.objects.get(id=id))
        return HttpResponse({"message": "Cancel Bill Added Successfully"})

@api_view(['GET', 'POST'])
def sales_cancel_bill(request):
    if request.method == "GET":
        id = request.GET.get('id')
        print('sale id ', id)
        return HttpResponse({"id ": id})

    elif request.method == "POST":
        id = request.POST.get('id')
        print('sale id ', id)
        date = request.POST.get('cancel_date')
        print('cancel date ', date)
        reason = request.POST.get('reason')
        print('cancel reason ', reason)
        cancel_bill_data = Bill.objects.create(date=date, reason=reason,
            sale_id=Sales.objects.get(id=id))
        print(cancel_bill_data)
        return HttpResponse({"message": "Cancel Bill Added Successfully"})

sales_templates = [
    path('sales/', sales, name='sales'),
    path('view_sales/', view_sales, name='view_sales'),
    path('api/SearchbyName/', SearchbyName, name='SearchbyName'),
    path('reports/', reports, name='reports'),
    path('update_sales/', update_sales, name='update_sales'),
    path('api/sales/pay_bill/', sales_pay_bill, name='sales_pay_bill'),
    path('api/sales/comp_bill/', sales_comp_bill, name='sales_comp_bill'),
    path('api/sales/cancel_bill/', sales_cancel_bill, name='sales_cancel_bill'),
]
