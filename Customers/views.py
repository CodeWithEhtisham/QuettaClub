from multiprocessing.sharedctypes import Value
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from Sales.models import Sales, Bill
from Sales.serializer import SalesSerializer
from .models import Customers
import pandas as pd
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CustomersSerializer
from django.utils import timezone
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count


def long_process(df):
    try:
        df.rename(columns=df.iloc[0], inplace=True)
        df.drop(df.index[0], inplace=True)
        # rename columns
        df.rename(columns={'Name': 'customer_name', 'Rank': 'customer_rank',
                           'Ser No ': 'customer_id'}, inplace=True)
        print(df.columns)
        cols = ['customer_name', 'customer_rank', 'customer_id']
        df = df[cols]
        df = df.to_dict('records')
        print(df)
        model_isntance = [Customers(**data) for data in df]
        obj = Customers.objects.bulk_create(model_isntance)
        print(obj)
        print("success")
        return True
    except Exception as e:
        print("failed", e)
        return False

##################################### Add & details Customer Functions ###


def signin(request):
    if request.method == 'POST':
        try:
            if request.POST.get('login_button'):
                username = request.POST.get('username')
                password = request.POST.get('password')
                # user = authenticate(username=username, password=password)
                # print('user: ', user)
                # if user is not None and user.is_active and user.is_authenticated:
                #     login(request, user)
                #     messages.success(request, f"You are now logged in as {username}")
                #     return redirect('index')
                # else:
                #     messages.error(request, "Invalid Credentials")
                #     return redirect('Customers:signin')
                if User.objects.get(username=username):
                    user = User.objects.get(username=username)
                    auth = authenticate(
                        username=user.username, password=password)
                    print('user: ', user)
                # if user is not None and user.is_authenticated:
                    if auth:
                        print('auth')
                        login(request, user)
                        messages.success(
                            request, f"You are now logged in as {username}")
                        return HttpResponseRedirect(reverse('Customers:index'))
                    else:
                        print('user login failed')
                        messages.error(request, "Invalid username or password")
                        return HttpResponseRedirect(reverse('Customers:signin'))
                else:
                    print('user login failed')
                    messages.error(request, "Invalid user")
                    return HttpResponseRedirect(reverse('Customers:signin'))
        except Exception as e:
            print('login error', e)
            messages.error(request, "Invalid user")
            return HttpResponseRedirect(reverse('Customers:signin'))
    else:
        return render(request, 'Customers/signin.html')




@login_required
def index(request):

    return render(request, "index.html")

def logout_user(request):
    logout(request)
    return render(request, 'Customers/signin.html')
@login_required
def customers(request):
    if request.method == 'POST':
        try:
            if request.POST.get('Save'):
                if Customers.objects.filter(
                        customer_address=request.POST.get('customer_address'),
                        customer_name=request.POST.get("customer_name"),
                        customer_rank=request.POST.get('customer_rank')).exists():
                    messages.error(request, 'Customer is Already Exists')
                    return redirect('Customers:customers')
                if Customers.objects.filter(customer_id=request.POST.get('customer_id')).exists():
                    messages.error(request, 'Customer ID is Already Exists')
                    return redirect('Customers:customers')
                else:
                    Customers(customer_name=request.POST.get('customer_name'),
                              customer_rank=request.POST.get('customer_rank'),
                              customer_id=request.POST.get('customer_id'),
                              customer_address=request.POST.get(
                                  'customer_address'),
                              customer_file=request.FILES.get('customer_file')).save()
                    messages.success(request, 'Customer Added Successfully')
                    return HttpResponseRedirect(reverse('Customers:customers'))
            elif request.POST.get('customer_file_submit'):
                # print("customer_file_submit")
                csv = request.FILES['customer_file']
                if not csv.name.split('.')[1] in ['csv', 'xlsx', 'xls']:
                    messages.error(
                        request, 'This is not a correct formate file')
                    return HttpResponseRedirect(reverse('Customers:customers'))
                else:
                    myfile = request.FILES["customer_file"]
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name, myfile)
                    uploaded_file_url = fs.url(filename)
                    excel_file = uploaded_file_url
                    print("." + excel_file)
                    print(csv.name.split('.')[-1])
                    if csv.name.split('.')[-1] in ['csv', 'CSV']:
                        df = pd.read_csv("." + excel_file)
                        if long_process(df):
                            messages.success(request, 'csv added to database')
                            return HttpResponseRedirect(reverse('Customers:customers'))
                    elif csv.name.split('.')[-1] in ['xlsx', 'XLSX', 'xls', 'XLS']:
                        print("excel")
                        df = pd.read_excel("." + excel_file)
                        if long_process(df):
                            messages.success(
                                request, 'excel added to database')
                            return HttpResponseRedirect(reverse('Customers:customers'))

                    raise Exception("File not found")
            # if request.POST.get('edit_customer'):
            # return render(request, "Customers/customer_update.html",
            # {'customer_data':
            # Customers.objects.filter(id=request.POST.get("cid"))[0]})

        except Exception as e:  # Exception as e:
            messages.error(request, 'Customer Added Failed {}'.format(e))
            return HttpResponseRedirect(reverse('Customers:customers'))
    else:
        return render(request, 'Customers/customers.html',
                      {'customers': Customers.objects.all().order_by("-id"),
                      'total_bills_amount': Sales.objects.values('customer_id').annotate(bills_count=Count('bill_no'), total_amount=Sum('net_amount')),
                       })


@login_required
def customer_update(request):
    if request.method == 'POST':
        try:
            if request.POST.get('update_customer'):
                Customers.objects.filter(id=request.POST.get('cid')).update(
                    customer_name=request.POST.get('customer_name'),
                    customer_rank=request.POST.get('customer_rank'),
                    customer_id=request.POST.get('customer_id'),
                    customer_address=request.POST.get('customer_address'))
                messages.success(request, 'Customer Updated Successfully')
                return HttpResponseRedirect(reverse('Customers:customers'))
        except Exception as e:
            messages.error(request, 'Customer Update Failed {}'.format(e))
            return HttpResponseRedirect(reverse('Customers:customers'))
    else:
        return render(request, "Customers/customer_update.html",
                      {'customer_data': Customers.objects.filter(id=request.GET.get("id")).first()})


@login_required
def customer_details(request):
    print(Sales.objects.filter(customer_id__id=request.GET.get(
        "id")).select_related('customer_id').order_by("-id"))
    if request.method == "POST":
        if request.POST.get('check'):
            value = request.POST.get('check')
            if value == 'all_check':
                print('all check')
                return render(request, 'Customers/customer_details.html', {
                    'all_bills': Bill.objects.all().select_related('sale_id').order_by('-id')
                })
            elif value == 'paid_check':
                print('paid check')
                return render(request, 'Customers/customer_details.html', {
                    'paid': Bill.objects.filter(status='Paid').select_related('sale_id').order_by('-id')
                })
            elif value == 'comp_check':
                print('complementary check')
                return render(request, 'Customers/customer_details.html', {
                    'paid': Bill.objects.filter(status='Complementery').select_related('sale_id').order_by('-id')
                })
            elif value == 'cancel_check':
                print('cancel check')
                return render(request, 'Customers/customer_details.html', {
                    'paid': Bill.objects.filter(status='Cancel').select_related('sale_id').order_by('-id')
                })
            else:
                print('no check')
                return render(request, 'Customers/customer_details.html')
    return render(request, "Customers/customer_details.html", {
        'Sales_data': Sales.objects.filter(customer_id__id=request.GET.get("id")).select_related('customer_id').order_by("-id")
    })


@login_required
def customer_bill(request):
    if request.method == 'POST':
        if request.POST.get('save_bill'):
            if Bill.objects.filter(sale_id__id=request.POST.get('sale_id')).exists():
                messages.error(request, 'This Bill No is Already Exists')
                return redirect('Customers:customer_bill')
            customer = Customers.objects.filter(
                customer_name=request.POST.get('customer_name'),
                customer_rank=request.POST.get('customer_rank')).first()

            Sales(bill_no=request.POST.get('bill_no'),
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
                  ).save()
            messages.success(request, 'Sales Added Successful')
            return redirect("Customers:customers")
            # return HttpResponse("success")
    else:
        return render(request, 'Customers/customer_bill.html', {
            'customer_data': Customers.objects.filter(id=request.GET.get("id")).first(),
            'sales': Sales.objects.all()
        })


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
            return Response(CustomersSerializer(Customers.objects.filter(customer_id__exact=value).order_by('-id'), many=True).data)
        elif field == 'Address':
            return Response(CustomersSerializer(Customers.objects.filter(customer_address__icontains=value).order_by('-id'), many=True).data)

    except Exception as e:
        return Response({"message": "No data found {}".format(e)})


@api_view(['GET', 'POST'])
def pay_bill(request):

    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        rv_no = request.POST.get('rv_no')
        paid_date = request.POST.get('paid_date')
        amount = request.POST.get('amount')
        remaining_amount = request.POST.get('remaining_amount')
        print("remaining amount ", remaining_amount)

        Bill.objects.create(rv_no=rv_no, date=paid_date, amount=amount,
                            status="Paid", sale_id=Sales.objects.get(id=id))

        Sales.objects.filter(id=id).update(net_amount=remaining_amount)

        print("sale net amount ", Sales.objects.filter(id=id).first())
        return Response({"message": "Bill Paid Successfully"})


@api_view(['GET', 'POST'])
def comp_bill(request):
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
def cancel_bill(request):

    if request.method == "POST":
        id = request.POST.get('id')
        date = request.POST.get('cancel_date')
        reason = request.POST.get('reason')
        remaining_amount = request.POST.get('remaining_amount')
        amount = request.POST.get('amount')
        Bill.objects.create(date=date, reason=reason,
                            status='Cancel', sale_id=Sales.objects.get(id=id))

        remaining_amount = 0
        amount = 0
        Sales.objects.filter(id=id).update(amount=amount ,net_amount=remaining_amount)
        messages.success(request, "Bill Cancelled Successfully")
        return HttpResponse({"message": "Cancel Bill Added Successfully"})

# urls paths and apis
index_template = [
    path('', signin, name='signin'),
    path('signin/', signin, name='signin'),
    path('index/', index, name='index'),
    path('customers/', customers, name='customers'),
    path('customer_details/', customer_details, name='customer_details'),
    path('customer_update/', customer_update, name='customer_update'),
    path('customer_bill/', customer_bill, name='customer_bill'),
    path('logout', logout_user, name='logout'),
    # api url paths
    path('api/SearchCustomer/', SearchCustomer, name='SearchCustomer'),
    path('api/customer/pay_bill/', pay_bill, name='pay_bill'),
    path('api/customer/comp_bill/', comp_bill, name='comp_bill'),
    path('api/customer/cancel_bill/', cancel_bill, name='cancel_bill'),
]
