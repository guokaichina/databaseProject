from django.shortcuts import render
from . import databaseApi
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . import models
import os

# Create your views here.


def index(request):
    # 商品目录展示
    if request.session.get('customer_id'):
        obj_customer = models.Customer.objects.get(pk=request.session['customer_id'])
        return render(request, 'index.html', {'customerName': obj_customer.customerName,
                                              'customerID': obj_customer.customerID})
    if request.session.get('seller_id'):
        obj_seller = models.Seller.objects.get(pk=request.session['seller_id'])
        return render(request, 'index.html', {'sellerName': obj_seller.sellerName,
                                              'sellerID': obj_seller.sellerID})
    else:
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
            else:
                msg = '用户名或密码错误'
                return render(request, 'login.html', {'msg': msg})
        elif request.POST.get('sellerName'):
            seller_name = request.POST['sellerName']
            password = request.POST['password']
            seller_id = databaseApi.seller_login_by_name(seller_name, password)
            if seller_id:
                request.session['seller_id'] = seller_id
                msg = '用户名或密码错误'
                return render(request, 'login.html', {'msg': msg})
            else:
                return HttpResponseRedirect(reverse('login'))
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
                msg = '用户名或邮箱已被使用'
                return render(request, 'register.html', {'msg': msg})
        elif request.POST.get('sellerName'):
            seller_name = request.POST['sellerName']
            password = request.POST['password']
            mail_address = request.POST['mailAddress']
            phone_number = request.POST['phoneNumber']
            if databaseApi.create_seller(seller_name, mail_address, password, phone_number, ''):
                return HttpResponseRedirect(reverse('login'))
            else:
                msg = '用户名或邮箱已被使用'
                return render(request, 'register.html', {'msg': msg})
    else:
        return render(request, 'register.html')


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('login'))


def goods_page(request, goods_id):
    #
    try:
        goods = models.Goods.objects.get(pk=goods_id)
    except models.Goods.DoesNotExist:
        return render(request, 'no_goods.html')
    # 商品下架检测
    if request.method == "POST":  # ajax
        customer_id = request.session.get('customer_id')
        if customer_id is None:
            return HttpResponse('0')  # 要求登录
        if request.POST['behavior'] == 'intended_goods':
            quantity = request.POST['quantity']
            databaseApi.create_intended_goods(customer_id, goods_id, quantity)
            return HttpResponse('1')
        if request.POST['behavior'] == 'buy':
            quantity = int(request.POST['quantity'])
            ship_to_address = request.POST['shipToAddress']
            databaseApi.create_order(customer_id, goods_id, quantity, ship_to_address)
            return HttpResponse('1')
    else:
        comment_list = databaseApi.show_comment(goods_id)
        goods_photo = models.Photos.objects.get(goods_id=goods_id)
        return render(request, 'goods_page.html', {'goods': goods, 'commentList': comment_list,
                                                   'goodsPhoto': goods_photo})


def shopping_cart(request, customer_id):
    # 登录检测
    login_id = request.session.get('customer_id')
    if login_id != customer_id:
        return HttpResponseRedirect('login')
    # 登录页面
    if request.method == 'POST':  # jsPost
        if request.POST['behavior'] == 'delete':
            goods_id = request.POST['goodsId']
            databaseApi.delete_intended_goods(customer_id, goods_id)
            return HttpResponseRedirect(reverse('shopping_cart'))
        elif request.POST['behavior']:  # buy
            goods_id = request.POST['goodsId']
            quantity = request.POST['quantity']
            ship_to_address = request.POST['shipToAddress']
            databaseApi.delete_intended_goods(customer_id, goods_id)
            order_id = databaseApi.create_order(customer_id, goods_id, quantity, ship_to_address)
            return HttpResponseRedirect(reverse('order', args=(order_id,)))
    intended_goods_list = databaseApi.show_intended_goods(customer_id)
    return render(request, 'shopping_cart.html', {'intendedGoodsList': intended_goods_list})


def order(request, customer_id):
    login_id = request.session.get('customer_id')
    if login_id != customer_id:
        return HttpResponseRedirect('login')
    if request.method == 'POST':  # ajax?
        if request.POST['behavior'] == 'cancel':
            order_id = request.POST['order_id']
            if databaseApi.cancel_order(order_id):
                return HttpResponseRedirect(reverse('order', args=(customer_id, )))
            else:
                return HttpResponseRedirect(reverse('order', args=(customer_id, )))
    order_list = databaseApi.show_order(customer_id)
    return render(request, 'order.html', {'orderList': order_list})


def order_message(request, customer_id, order_id):
    login_id = request.session.get('customer_id')
    if login_id != customer_id:
        return HttpResponseRedirect('login')
    order_info = models.Order.objects.get(pk=order_id)
    return render(request, 'order_message.html', {'order': order_info})


def goods_management(request, seller_id):
    login_id = request.session.get('seller_id')
    if login_id != seller_id:  # 未登录页面
        return HttpResponseRedirect(reverse('login'))
    # 进入对应的商品管理页面
    if request.method == 'POST':
        if request.POST['behavior'] == 'delete':
            goods_id = int(request.POST['goodsId'])
            photo_path = models.Photos.objects.get(goodsID=goods_id)  # 查找对应图片
            path = "../static/picture/" + photo_path
            os.remove(path)  # 删除对应图片
            databaseApi.delete_goods(goods_id)  # 由于完整性约束，删掉对应的图片
            msg = '删除成功'
            return render(request, 'goods_management.html', {'msg': msg})
        elif request.POST['behavior'] == 'change':
            goods_id = request.POST['goodsId']
            goods_name = request.POST['goodsName']
            goods_stock = request.POST['goodsStock']
            goods_price = request.POST['goodsPrice']
            goods = models.Goods.objects.get(pk=goods_id)
            goods.goodsName = goods_name
            goods.goodsStock = goods_stock
            goods.goodsPrice = goods_price
            goods.save()
            msg = '改变成功'
            return render(request, 'goods_management.html', {'msg': msg})
    else:
        obj_seller = models.Seller.objects.get(pk=seller_id)
        goods_management_list = databaseApi.show_goods_for_management(seller_id)
        return render(request, 'goods_management.html', {'sellerId': seller_id,
                                                         'sellerName': obj_seller.sellerName,
                                                         'goodsManagementList': goods_management_list})


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
        goods_image = request.FILES['goodsImage']
        extension_name = request.POST['extensionName']
        goods_id = databaseApi.create_goods(seller_id, goods_name, goods_stock, goods_price, goods_type)
        if goods_id:
            photo_id = databaseApi.create_photo_path(goods_id, extension_name)
            path = "../static/picture/" + str(photo_id) + extension_name  # 路径设计
            handle_uploaded_file(goods_image, path)  # 保存
            msg = '提交成功'
            return render(request, 'goods_add.html', {'msg': msg})
        # 提交商品成功
        else:
            msg = '失败，请检查是否有输入格式上的错误'
            return render(request, 'goods_add.html', {'msg': msg})
    else:
        return render(request, 'goods_add.html')


def search_goods(request, keyword=''):
    if request.GET.get('keyword'):
        keyword = request.GET['keyword']
        print('ok')
        return HttpResponseRedirect(reverse('search_goods', args=(keyword, )))

    return render(request, 'search.html', {'keyword': keyword})


def test_page(request):
    # 用于临时显示首页
    return HttpResponseRedirect(reverse('index'))


def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
