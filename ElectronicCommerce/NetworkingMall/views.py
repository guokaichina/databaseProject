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
        elif request.POST.get('sellerName'):
            seller_name = request.POST['sellerName']
            password = request.POST['password']
            seller_id = databaseApi.seller_login_by_name(seller_name, password)
            if seller_id:
                request.session['seller_id'] = seller_id
                return HttpResponseRedirect(reverse('index'))
    # 顾客商家登录基本功能
    else:
        return render(request, 'login.html')
    # get方式获得网页


def register(request):
    #
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
        elif request.POST.get('sellerName'):
            seller_name = request.POST['sellerName']
            password = request.POST['password']
            mail_address = request.POST['mailAddress']
            phone_number = request.POST['phoneNumber']
            if databaseApi.create_seller(seller_name, mail_address, password, phone_number, ''):
                return HttpResponseRedirect(reverse('login'))
            else:
                return HttpResponseRedirect(reverse('register'))

    # 登录时的post
    return render(request, 'register.html')


def customer(request, customer_id):
    # 登录状态检测
    login_id = request.session.get('customer_id')
    if login_id != customer_id:
        return HttpResponseRedirect('login')
    # 登录状态检测
    return render(request, 'customer.html')


def goods_page(request, goods_id):
    #
    try:
        models.Goods.objects.get(pk=goods_id)
    except models.Goods.DoesNotExist:
        return render(request, 'no_goods.html')
    # 商品下架检测
    return render(request, 'goods_page.html')


def shopping_cart(request, customer_id):
    # 登录检测
    login_id = request.session.get('customer_id')
    if login_id != customer_id:
        return HttpResponseRedirect('login')
    # 登录页面
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


def goods_add(request, seller_id):
    login_id = request.session.get('seller_id')
    if login_id != seller_id:  # 未登录页面
        return HttpResponseRedirect(reverse('login'))
    # 进入添加商品页面
    # def create_goods(seller_id, goods_name, goods_stock, goods_price, goods_type):
    if request.POST.get('goodsName'):
        goods_name = request.POST['goodsName']
        goods_stock = request.POST['goodsStock']
        goods_price = request.POST['goodsPrice']
        goods_type = request.POST['goodsType']
        goods_image = request.POST['goodsImage']
        goods_id = databaseApi.create_goods(seller_id, goods_name, goods_stock, goods_price, goods_type)
        if goods_id:
            pass
        picture_file = open(goods_name, 'wb')
        picture_file.write(goods_image)
        # 提交商品成功

    else:
        return render(request, 'goods_add.html')


def test_page(request):
    # 用于临时显示首页
    return HttpResponseRedirect(reverse('login'))


def do_something(arg):
    pass
    return


def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
