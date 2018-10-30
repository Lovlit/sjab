from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from rest_framework.views import APIView
from . serializers import ItemSerializer
from rest_framework.response import Response

# Create your views here.
from django.template import RequestContext

from inventory.forms import ItemForm, ItemWarehouseForm
from inventory.models import ItemWarehouseMapping, Item, Warehouse, Voucher, VoucherItemMapping


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('accounts/profile/')
        else:
            msg ="Username or Password is incorrect."
            return render_to_response('registration/login.html', {'msg': msg})

    return render(request, 'registration/login.html')


def log_out(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/')


@login_required(login_url='/login')
def index(request):
    items = Item.objects.filter()
    html_data = []
    warehouse = Warehouse.objects.filter().order_by('id')
    for data in items:
        item_stock = []
        for ware in warehouse:
            stock = ItemWarehouseMapping.objects.filter(item_id=data.id, warehouse_id=ware.id).order_by('warehouse_id')
            if not stock:
                stock = 0
            else:
                stock = stock[0].stock
            item_stock.append(stock)
        values = {'name': data.name, 'stock': item_stock}
        html_data.append(values)
    return render(request, 'inventory/index2.html', {'warehouse': warehouse, 'item': html_data})


@login_required(login_url='/accounts/login/')
def additem(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form_item = ItemForm(request.POST)

        # check if it's valid:
        if form_item.is_valid():
            # Insert into DB
            form_item.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/accounts/profile')
    else:
        # GET, generate unbound (blank) form

        form_item = ItemForm()
    return render(request, 'inventory/add_item.html', {'form_item': form_item})


@login_required(login_url='/accounts/login/')
def voucherlist(request):
    voucher_names = Voucher.objects.filter().order_by('-date_issued')
    return render(request, 'inventory/vouchers.html', {'voucher_names': voucher_names})


@login_required(login_url='/accounts/login/')
def voucherinfo(request):
    pk = request.GET.get('pk')
    if pk:
        voucher = VoucherItemMapping.objects.filter(voucher_number_id=pk)
    else:
        voucher = []
    return render(request, 'inventory/voucher_info.html', {'voucher': voucher})


@login_required(login_url='/accounts/login/')
def createvoucher(request):
    warehouse = Warehouse.objects.filter()
    data_dict = ""
    item = Item.objects.filter()
    for data in item:
        data_dict = data_dict + ',' + data.name
    if request.method == 'POST':
        issued_by = request.POST['issued_by']
        issued_to = request.POST['issued_to']
        voucher = Voucher(issued_by=issued_by, issued_to=issued_to)
        voucher.save()
        vouchernumber = Voucher.objects.latest('id')
        warehouse_name = request.POST['warehouse_name']
        item_name = request.POST['item_name']
        quantity =request.POST['quantity']
        ware_id = Warehouse.objects.filter(name=warehouse_name).only('id')
        item_id =Item.objects.filter(name=item_name).only('id')
        voucher_detail = VoucherItemMapping(voucher_number=vouchernumber, warehouse=warehouse_name, item=warehouse_name, quantity=quantity)
        voucher_detail.save()

        return HttpResponseRedirect('createvoucher')

    return render(request, 'inventory/generate_voucher.html', {'warehouse': warehouse, 'data_dict': data_dict})


class Test(View):
    items = ItemWarehouseMapping.objects.all()
    post_req = 'this is post request'
    form = ItemForm

    def get(self, request):
         return render(request, 'inventory/test_class_view.html', {'items': self.items, 'form': self.form})

    def post(self, request):

        form=ItemForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('test')


class ItemApi(APIView):

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self):
        pass