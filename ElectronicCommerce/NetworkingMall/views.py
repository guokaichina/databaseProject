from django.shortcuts import render
from . import databaseApi
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . import models
import os


def index(request):
    # 商品目录展示
    context = {}
    login_message(request, context)
    #  ('1', '女装'), ('2', '男装'), ('3', '食品'), ('4', '医药'), ('5', '日用'),('8', '电子')
    list_1 = models.Goods.objects.filter(goodsType='女装').order_by('-goodsID')[:6]
    list_2 = models.Goods.objects.filter(goodsType='男装').order_by('-goodsID')[:6]
    list_3 = models.Goods.objects.filter(goodsType='食品').order_by('-goodsID')[:6]
    list_4 = models.Goods.objects.filter(goodsType='医药').order_by('-goodsID')[:6]
    list_5 = models.Goods.objects.filter(goodsType='日用').order_by('-goodsID')[:6]
    list_6 = models.Goods.objects.filter(goodsType='电子').order_by('-goodsID')[:6]
    context.update({'type1': list_1, 'type2': list_2, 'type3': list_3, 'type4': list_4, 'type5': list_5,
                    'type8': list_6})
    return render(request, 'index.html', context)


def login(request):
    #
    if request.session.get('customer_id'):
        return HttpResponseRedirect(reverse('index'))
    if request.session.get('seller_id'):
        seller_id = request.session['seller_id']
        return HttpResponseRedirect(reverse('seller_index', args=(seller_id,)))
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
    return HttpResponseRedirect(reverse('index'))


def goods_page(request, goods_id):
    #
    try:
        goods = models.Goods.objects.get(pk=goods_id)
    except models.Goods.DoesNotExist:
        return render(request, 'no_goods.html')
    # 商品下架检测
    context = {}
    if request.method == "POST":
        customer_id = request.session.get('customer_id')
        if customer_id is None:
            context['msg'] = '请登录'
        if request.POST['behavior'] == 'addCart':
            quantity = int(request.POST['quantity'])
            goods_id = int(request.POST['goodsId'])
            databaseApi.create_intended_goods(customer_id, goods_id, quantity)
            context['msg'] = '加入购物车成功'
        if request.POST['behavior'] == 'buy':
            if buy(request, customer_id):
                return HttpResponseRedirect(reverse('order', args=(customer_id, )))
            else:
                context['msg'] = '购买失败，密码输入错误'
    login_message(request, context)
    comment_list = databaseApi.show_comment(goods_id)
    goods_photo = models.Photo.objects.get(goodsID=goods_id)
    context['goods'] = goods
    context['commentList'] = comment_list
    context['goodsPhoto'] = goods_photo
    return render(request, 'goods_page.html', context)


def shopping_cart(request, customer_id):
    # 登录检测
    login_id = request.session.get('customer_id')
    if login_id != customer_id:
        return HttpResponseRedirect('login')
    # 登录页面
    context = {}
    login_message(request, context)
    if request.method == 'POST':  # jsPost
        if request.POST['behavior'] == 'delete':
            intended_goods_id = int(request.POST['intendedGoodsId'])
            databaseApi.delete_intended_goods(intended_goods_id)
            context['msg'] = '删除成功'
        elif request.POST['behavior'] == 'deleteCartAll':
            models.IntendedGoods.objects.filter(customerID=customer_id).delete()
            context['msg'] = '清空购物车成功'
        elif request.POST['behavior'] == 'buy':
            # 密码检测
            password = request.POST['password']
            customer = models.Customer.objects.get(pk=customer_id)
            if password != customer.password:
                context['msg'] = '购买失败，密码错误'
            else:
                ship_to_address = request.POST['shipToAddress']
                request.session['shipToAddress'] = ship_to_address
                intended_goods_array = request.POST['intendedGoodsArray'].split(',')
                for intended_goods_id in intended_goods_array:
                    intended_goods = models.IntendedGoods.objects.get(pk=int(intended_goods_id))
                    goods_id = intended_goods.goodsID.goodsID
                    quantity = intended_goods.quantity
                    databaseApi.create_order(customer_id, goods_id, quantity, ship_to_address)
                    intended_goods.delete()
                return HttpResponseRedirect(reverse('order', args=(customer_id, )))
        elif request.POST['behavior'] == 'add':
            intended_goods_id = request.POST['intendedGoodsId']
            intended_goods = models.IntendedGoods.objects.get(pk=intended_goods_id)
            intended_goods.quantity += 1
            intended_goods.save()
            return HttpResponse(intended_goods.quantity)
        elif request.POST['behavior'] == 'minus':
            intended_goods_id = request.POST['intendedGoodsId']
            intended_goods = models.IntendedGoods.objects.get(pk=intended_goods_id)
            intended_goods.quantity -= 1
            intended_goods.save()
            return HttpResponse(intended_goods.quantity)
    intended_goods_list = databaseApi.show_intended_goods(customer_id)
    context['intendedGoodsList'] = intended_goods_list
    return render(request, 'shopping_cart.html', context)


def order(request, customer_id):
    login_id = request.session.get('customer_id')  # 登录检测
    if login_id != customer_id:
        return HttpResponseRedirect('login')
    customer = models.Customer.objects.get(pk=customer_id)
    context = {'customer': customer}
    if request.method == 'POST':
        order_id = int(request.POST['orderId'])
        if request.POST['behavior'] == 'cancel':
            if databaseApi.cancel_order(order_id):
                context['msg'] = '删除成功'
            else:
                context['msg'] = '删除失败，超过一天的订单不能取消，或商品已下架'
        elif request.POST['behavior'] == 'confirm':
            the_order = models.Order.objects.get(orderID=order_id)
            if not the_order.receivingStatus:
                the_order.receivingStatus = True
                the_order.save()
                context['msg'] = '确认收货'
            else:
                context['msg'] = '此商品已确认收货'
    order_list = databaseApi.show_order(customer_id)
    context['orderList'] = order_list
    return render(request, 'order.html', context)


def seller_index(request, seller_id):
    login_id = request.session.get('seller_id')
    if login_id != seller_id:  # 未登录页面
        return HttpResponseRedirect(reverse('login'))
    # 进入对应的商品管理页面
    context = {}
    if request.method == 'POST':
        if request.POST['behavior'] == 'delete':
            goods_id = int(request.POST['goodsId'])
            photo = models.Photo.objects.get(goodsID=goods_id)  # 查找对应图片
            path = "static/picture/" + photo.photoPath
            os.remove(path)  # 删除对应图片
            databaseApi.delete_goods(goods_id)  # 由于完整性约束，删掉对应的图片
            context['msg'] = '删除成功'
        elif request.POST['behavior'] == 'change':
            goods_id = int(request.POST['goodsId'])
            goods_name = request.POST['goodsName']
            goods_stock = request.POST['goodsStock']
            goods_price = request.POST['goodsPrice']
            goods = models.Goods.objects.get(pk=goods_id)
            goods.goodsName = goods_name
            goods.goodsStock = goods_stock
            goods.goodsPrice = goods_price
            goods.save()
            context['msg'] = '改变成功'
        elif request.POST['behavior'] == 'address':  # ajax
            shipping_address = request.POST['shippingAddress']
            seller = models.Seller.objects.get(pk=seller_id)
            seller.shippingAddress = shipping_address
            seller.save()
            return HttpResponse(shipping_address)
    obj_seller = models.Seller.objects.get(pk=seller_id)
    goods_management_list = databaseApi.show_goods_for_management(seller_id)
    context.update({'sellerId': seller_id, 'sellerName': obj_seller.sellerName,
                    'shippingAddress': obj_seller.shippingAddress,
                    'goodsManagementList': goods_management_list})
    return render(request, 'seller_index.html', context)


def goods_add(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('index'))
    seller_id = request.session.get('seller_id')
    goods_name = request.POST['goodsName']
    goods_stock = request.POST['goodsStock']
    goods_price = request.POST['goodsPrice']
    goods_type = request.POST['goodsType']
    goods_image = request.FILES['goodsImage']
    extension_name = request.POST['extensionName']
    goods_id = databaseApi.create_goods(seller_id, goods_name, goods_stock, goods_price, goods_type)
    if goods_id:
        photo_id = databaseApi.create_photo_path(goods_id, extension_name)
        path = "static/picture/" + str(photo_id) + extension_name  # 路径设计
        handle_uploaded_file(goods_image, path)  # 保存
        return HttpResponseRedirect(reverse('seller_index', args=(seller_id, )))
    else:
        return HttpResponseRedirect(reverse('seller_index', args=(seller_id, )))


def search_goods(request, keyword=''):
    context = {}
    search_type = ''
    login_message(request, context)
    if request.method == 'POST':  # 种类选择
        if request.POST.get('behavior'):
            if context.get('customerID'):  # 登录检测
                customer_id = context['customerID']
                if request.POST['behavior'] == 'addCart':
                    goods_id = request.POST['goodsId']
                    databaseApi.create_intended_goods(customer_id, goods_id, 1)  # 暂且为1
                    context['msg'] = '加入购物车成功'
                elif request.POST['behavior'] == 'buy':
                    if buy(request, customer_id):
                        return HttpResponseRedirect(reverse('order', args=(customer_id, )))
                    else:
                        context['msg'] = '密码输入错误'
            else:
                context['msg'] = '顾客未登录不能进行此操作'
        else:
            search_type = request.POST['goodsType']
            context['searchType'] = search_type
    search_list = databaseApi.get_search_list(keyword, search_type)
    context.update({'keyword': keyword, 'searchList': search_list})
    if request.session.get('shipToAddress'):
        context['shipToAddress'] = request.session['shipToAddress']
    return render(request, 'search.html', context)


def test_page(request):
    # 用于临时显示首页
    return HttpResponseRedirect(reverse('index'))


def handle_uploaded_file(f, path):
    with open(path, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def login_message(request, context):
    if request.session.get('customer_id'):
        obj_customer = models.Customer.objects.get(pk=request.session['customer_id'])
        context['customerName'] = obj_customer.customerName
        context['customerID'] = obj_customer.customerID
        context['customer'] = obj_customer
    elif request.session.get('seller_id'):
        obj_seller = models.Seller.objects.get(pk=request.session['seller_id'])
        context['sellerName'] = obj_seller.sellerName
        context['sellerID'] = obj_seller.sellerID


def buy(request, customer_id):
    password = request.POST['password']
    customer = models.Customer.objects.get(pk=customer_id)
    if password != customer.password:
        return False
    goods_id = int(request.POST['goodsId'])
    ship_to_address = request.POST['shipToAddress']
    request.session['shipToAddress'] = ship_to_address
    quantity = int(request.POST['quantity'])
    databaseApi.create_order(customer_id, goods_id, quantity, ship_to_address)
    return True
