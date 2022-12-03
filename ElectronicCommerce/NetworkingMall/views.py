from django.shortcuts import render
from . import databaseApi
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import models
# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    #
    if request.session.get('customer_id'):
        return HttpResponseRedirect(reverse('index'))
    if request.session.get('seller_id'):
        seller_id = request.session['seller_id']
        return HttpResponseRedirect(reverse('goods_management', args=(seller_id,)))
    # 已登录时的强制跳转
    #
    if request.method == 'POST':
        if request.POST.get('customerName'):
            customer_name = request.POST['customerName']
            password = request.POST['password']
            customer_id = databaseApi.customer_login_by_name(customer_name, password)
            if customer_id:
                request.session['customer_id'] = customer_id
                return HttpResponseRedirect(reverse('index'))
    # 顾客商家登录基本功能
    else:
        return render(request, 'login.html')
    # get方式获得网页


def register(request):
    if request.method == 'POST':
        if request.POST.get('customerName'):
            customer_name = request.POST['customerName']
            password = request.POST['password']
            mail_address = request.POST['mailAddress']
            phone_number = request.POST['phoneNumber']
            if databaseApi.create_customer(customer_name, mail_address, password, phone_number):
                return HttpResponseRedirect(reverse('login'))
            else:
                return HttpResponseRedirect(reverse('register'))
    return render(request, 'register.html')


def customer(request, customer_id):
    login_id = request.session.get('customer_id')
    if login_id != customer_id:
        return HttpResponseRedirect('login')
    return render(request, 'customer.html')


def goods_page(request, goods_id):
    try:
        models.Goods.objects.get(pk=goods_id)
    except models.Goods.DoesNotExist:
        return render(request, 'no_goods.html')

    return render(request, 'goods_page.html')


def shopping_cart(request, customer_id):
    login_id = request.session.get('customer_id')
    if login_id != customer_id:
        return HttpResponseRedirect('login')
    return render(request, 'shopping_cart.html')


def order(request, customer_id):
    login_id = request.session.get('customer_id')
    if login_id != customer_id:
        return HttpResponseRedirect('login')
    return render(request, 'order.html')


def goods_management(request, seller_id):
    login_id = request.session.get('seller_id')
    if login_id != seller_id:  # 未登录页面
        return HttpResponseRedirect(reverse('login'))
    # 进入对应的商品管理页面
    do_something(seller_id)
    return render(request, 'goods_management.html')


def test_page(request):
    return render(request, 'register.html')


def do_something(arg):
    pass
    return
