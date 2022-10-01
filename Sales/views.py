
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.contrib import messages
from .models import Sales, Bill ,dummyTable
from Customers.models import Customers
import pandas as pd
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import SalesSerializer
from django.db.models import Sum
import datetime
import os

def long_process(df):
    try:
        # rename
        rename={
            "BILL No":'bill_no',
            "Rank":'rank',
            "POS No":'PoS_no',
            "Name":'cname',
            "Address":'address',
            "On Account Of":'account_of',
            "Dated":'date',
            "Month":'month',
            "Amount":'amount',
            "Discount ":'discount',
            "Net Amount":'net_amount'
        }
        df.rename(columns=rename, inplace=True)
        print(df.columns)
        for index,row in df.iterrows():
            print(row['cname'])
            if Customers.objects.filter(customer_name=row['cname'],
                customer_rank=row['rank'],customer_address=row['address']).exists():
                dummyTable.objects.create(
                    bill_no=row['bill_no'],
                    rank=row['rank'],
                    pos_no=row['PoS_no'],
                    cname=row['cname'],
                    address=row['address'],
                    account_of=row['account_of'],
                    date=row['date'],
                    month=row['month'],
                    amount=row['amount'],
                    discount=row['discount'],
                    net_amount=row['net_amount'],
                    status="already exists"

                ).save()
            else:
                dummyTable.objects.create(
                    bill_no=row['bill_no'],
                    rank=row['rank'],
                    pos_no=row['PoS_no'],
                    cname=row['cname'],
                    address=row['address'],
                    account_of=row['account_of'],
                    date=row['date'],
                    month=row['month'],
                    amount=row['amount'],
                    discount=row['discount'],
                    net_amount=row['net_amount'],
                    status="new"

                ).save()
        return True
    except Exception as e:
        print(e)
        return False

def sales(request):
    print("###############################################",request.method)
    if request.method == 'POST':
        try:
            if request.POST.get('Save'):
                print(request.POST.get('customer_name'))
                
                customer=Customers.objects.filter(customer_name=request.POST.get('customer_name'),customer_rank=request.POST.get('customer_rank'))
                print(customer)
                dummyTable.objects.create(
                                bill_no=request.POST.get('bill_no'),
                                rank=request.POST.get('customer_rank'),
                                pos_no=request.POST.get('PoS_no'),
                                cname=request.POST.get('customer_name'),
                                address=request.POST.get('address'),
                                account_of=request.POST.get('account_of'),
                                date=request.POST.get('date'),
                                month=request.POST.get('month'),
                                amount=request.POST.get('amount'),
                                discount=request.POST.get('discount'),
                                net_amount=request.POST.get('net_amount'),
                                remarks=request.POST.get('remarks'),
                                status="new" if not customer else "already exists"
                                ).save()

                messages.success(request, 'Sales Added Successful')
                return HttpResponseRedirect(reverse("Sales:sales"))
            
            elif request.POST.get('upload_bills'):
                
                messages.success(request, 'Sales Added Successful')
                return HttpResponseRedirect(reverse("Sales:sales"))

            elif request.POST.get('delete_all'):
                dummyTable.objects.all().delete()
                messages.success(request, "All today's Bills have been deleted successfully")
                return redirect('Sales:sales')

            elif request.POST.get('sale_file_submit'):
                print("customer_file_submit")
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
                        os.remove("."+excel_file)
                        if long_process(df):
                            messages.success(request, 'Sales csv Added Successful')
                            return HttpResponseRedirect(reverse("Sales:sales"))
                    elif csv.name.split('.')[-1] in ['xlsx','XLSX','xls','XLS']:
                        print("excel")
                        df = pd.read_excel("."+excel_file)
                        os.remove("."+excel_file)
                        if long_process(df):
                            messages.success(request, 'Sales excel Added Successful')
                            return HttpResponseRedirect(reverse("Sales:sales"))
                raise Exception("File not found") 
        except Exception as e:  # Exception as e:
                messages.error(request, 'Sales Added Failed',e)
                return HttpResponse("Please fill the required fields! Back to Sales page {}".format(e), status=400)

    else:
        print(dummyTable.objects.all())          
        return render(request, "Sales/sales.html", {
            'customers': Customers.objects.all(),
            'sales': Sales.objects.all(),
            'dummy': dummyTable.objects.all().order_by('-id'),
            })

def delete_items(request, pk):
	queryset = dummyTable.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		return redirect('Sales:sales')
	return render(request, 'Sales/delete_items.html',{
        'queryset': queryset
    })


def view_sales(request):
    if request.method == "POST":
        try:
            pass
        except Exception as e:
            pass
    else:
        return render(request, "Sales/view_sales.html",
                {'sales_data': Sales.objects.all().select_related('customer_id').order_by("-bill_no"),
                # exclude(created_on__date=timezone.now()).
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
                    customer_rank=request.POST.get('customer_rank'))

                dummyTable.objects.filter(id=request.POST.get('edit_id')).update(
                    bill_no=request.POST.get('bill_no'),
                    pos_no=request.POST.get('PoS_no'),
                    month=request.POST.get('month'),
                    date=request.POST.get('date'),
                    address=request.POST.get('address'),
                    account_of=request.POST.get('account_of'),
                    amount=request.POST.get('amount'),
                    discount=request.POST.get('discount'),
                    net_amount=request.POST.get('net_amount'),
                    remarks=request.POST.get('remarks'),
                    status="new" if not customer else "already exists",
                    cname=request.POST.get('customer_name'),
                    rank=request.POST.get('customer_rank'),
                    )
                
                return HttpResponseRedirect(reverse("Sales:sales"))
            if request.POST.get('cancel'):
                return HttpResponseRedirect(reverse("Sales:sales"))
        except Exception as e:
            messages.error(request, f'Sales Update Failed {e}')
            return HttpResponseRedirect(reverse("Sales:view_sales"))

    else:
        return render(request, "Sales/update_sales.html", {
                'sales_data': dummyTable.objects.filter(id=request.GET.get('id')).first()
            })


def reports(request):
    print(Sales.objects.filter(customer_id__id=request.GET.get(
        "id")).select_related('customer_id').order_by("-id"))
    if request.method == "POST":
        if request.POST.get("report_generate"):
            from_date = request.POST.get("from-date")
            to_date = request.POST.get("to-date")
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')

        if request.POST.get('check'):
            value = request.POST.get('check')
            if value == 'all_check':
            #     print('all check')
                pass               
            elif value == 'paid_check':
                print('paid check')
                return render(request, 'Sales/reports.html', {
                    'record': Bill.objects.filter(status='Paid').select_related('sale_id').order_by('-id')
                })
            elif value == 'comp_check':
                print('complementary check')
                return render(request, 'Sales/reports.html', {
                    'record': Bill.objects.filter(status='Complementery').select_related('sale_id').order_by('-id')
                })
            elif value == 'cancel_check':
                print('cancel check')
                return render(request, 'Sales/reports.html', {
                    'record': Bill.objects.filter(status='Cancel').select_related('sale_id').order_by('-id')
                })
            else:
                print('no check')
                return render(request, 'Sales/reports.html')
    
    return render(request, 'Sales/reports.html',{
                    'record': Bill.objects.all().select_related('sale_id').order_by('-id')
                })

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
        remaining_amount = request.POST.get('remaining_amount')
        amount = request.POST.get('amount')
        Bill.objects.create(date=date, reason=reason,
           status='Cancel', sale_id=Sales.objects.get(id=id))

        Sales.objects.filter(id=id).update(amount=amount ,net_amount=remaining_amount)
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


@api_view(['POST'])
def sales_upload(request):
    if request.method == "POST":
        jsons = request.data
        print(jsons['myrows'][0])
        for obj in jsons['myrows']:
            if Customers.objects.filter(customer_name=obj['Name'],customer_address=obj['Address']).exists():
                customer = Customers.objects.get(customer_name=obj['Name'],customer_address=obj['Address'])
                Sales.objects.create(
                    bill_no=obj['Bill No'],
                    PoS_no=obj['POS NO'],
                    created_date=datetime.datetime.strptime(obj['Dated'], '%d-%m-%Y').strftime('%Y-%m-%d'),
                    month=obj['Month'],
                    account_of=obj['On Account Of'],
                    amount=obj['Amount'],
                    net_amount=obj['Net Amount'],
                    discount=obj['Discount'],
                    customer_id=customer
                ).save()
            else:
                customer=Customers.objects.create(
                    customer_name=obj['Name'],
                    customer_address=obj['Address'],
                    customer_rank=obj['Rank']
                )
                customer.save()
                Sales.objects.create(
                    bill_no=obj['Bill No'],
                    PoS_no=obj['POS NO'],
                    created_date=datetime.datetime.strptime(obj['Dated'], '%d-%m-%Y').strftime('%Y-%m-%d'),
                    month=obj['Month'],
                    account_of=obj['On Account Of'],
                    amount=obj['Amount'],
                    net_amount=obj['Net Amount'],
                    discount=obj['Discount'],
                    customer_id=customer
                ).save()
        dummyTable.objects.all().delete()
        return Response({"message": "Sales Data Uploaded Successfully"})
    else:
        return Response({"message": "Sales Data Not Uploaded"})
            


        return Response({"message": "Data Uploaded Successfully"})

sales_templates = [
    path('sales/', sales, name='sales'),
    path('view_sales/', view_sales, name='view_sales'),
    path('api/SearchbyName/', SearchbyName, name='SearchbyName'),
    path('reports/', reports, name='reports'),
    path('update_sales/', update_sales, name='update_sales'),
    path('delete_items/<str:pk>/', delete_items, name="delete_items"),
    path('api/sales/pay_bill/', sales_pay_bill, name='sales_pay_bill'),
    path('api/sales/comp_bill/', sales_comp_bill, name='sales_comp_bill'),
    path('api/sales/cancel_bill/', sales_cancel_bill, name='sales_cancel_bill'),
    path('api/sales/sales_upload/', sales_upload, name='sales_upload')
]
