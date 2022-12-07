from .models import *
import django.core.exceptions


def create_customer(customer_name, mail_address, password, phone_number):
    # 在数据库中创建一个customer，返回bool值， 创建成功则返回True， 创建失败(mail_address重复或customer重复)返回False
    try:
        customer_set_1 = Customer.objects.filter(customerName=customer_name)
        customer_set_2 = Customer.objects.filter(mailAddress=mail_address)

        if customer_set_1.exists() and customer_set_2.exists():
            # '''print('用户名已被占用; 邮箱已注册账号')'''
            return False
        elif customer_set_1.exists():
            # '''print('用户名已被占用')'''
            return False
        elif customer_set_2.exists():
            # '''print('邮箱已注册账号')'''
            return False
        else:
            Customer.objects.create(customerName=customer_name, mailAddress=mail_address,
                                    password=password, phoneNumber=phone_number)
            return True
    except django.core.exceptions:
        # print('创建顾客用户异常')
        return False


def create_seller(seller_name, mail_address, password, phone_number, shipping_address):
    # 在数据库中创建一个seller, 返回bool值， 成功返回True， 用户名重复、邮箱重复或创建失败返回False 同样，检测mail_address，seller_name的重复性
    try:
        seller_set_1 = Seller.objects.filter(sellerName=seller_name)
        seller_set_2 = Seller.objects.filter(mailAddress=mail_address)
        if seller_set_1.exists() and seller_set_2.exists():
            # '''print('用户名已被占用; 邮箱已注册账号')'''
            return False
        elif seller_set_1.exists():
            # '''print('用户名已被占用')'''
            return False
        elif seller_set_2.exists():
            # '''print('邮箱已注册账号')'''
            return False
        else:
            Seller.objects.create(sellerName=seller_name, mailAddress=mail_address,
                                  password=password, phoneNumber=phone_number, shippingAddress=shipping_address)
            return True
    except django.core.exceptions:
        # print('创建商家用户异常')
        return False


def create_goods(seller_id, goods_name, goods_stock, goods_price, goods_type):
    # 在数据库goods表，创建一个新的商品,创建成功返回goodsID，创建失败返回0
    # 暂时先返回goods_id
    try:
        seller = Seller.objects.get(sellerID=seller_id)
        goods = Goods.objects.create(goodsName=goods_name, goodsStock=goods_stock, goodsSold=0, goodsPrice=goods_price,
                                     goodsType=goods_type, sellerID=seller)
        return goods.goodsID
    except django.core.exceptions:
        # print('create_goods_error:添加新商品失败')  # 创建商品失败
        return 0


def create_photo_path(goods_id, extension_name):
    # 在数据库Photos表中，插入一个元组，成功创建返回ID,失败则返回0
    try:
        goods = Goods.objects.get(goodsID=goods_id)
        photo = Photos.objects.create(photoPath=extension_name, goodsID=goods)
        photo.photoPath = str(photo.photoID) + extension_name
        photo.save()
        return photo.photoID
    except django.core.exceptions:
        # print("add_photo_error:添加新图片失败")
        return 0


def create_intended_goods(customer_id, goods_id, quantity):
    # 意向商品表中插入一项 不需要返回值
    try:
        customer = Customer.objects.get(customerID=customer_id)
        goods = Goods.objects.get(goodsID=goods_id)
        IntendedGoods.objects.create(
            goodsID=goods, customerID=customer, quantity=quantity)
        return True
    except django.core.exceptions:
        # print('添加意向商品失败')
        return False


def create_order(customer_id, goods_id, quantity, ship_to_address):
    # 订单表中创建一项order
    # amount, goodsName, customerName, sellerName,createTime 通过查找数据库计算得出
    # 注意，此处创建订单的行为和购买一致，因此需要对goods的库存进行修改
    try:
        customer = Customer.objects.get(customerID=customer_id)
        goods = Goods.objects.get(goodsID=goods_id)
        seller = Seller.objects.filter(goods__goodsID=goods_id)
        # 这里需要检测，goodsStock减去过后是否大于0
        goods.goodsStock -= quantity
        goods.goodsSold += quantity
        goods.save()
        order = Order.objects.create(amount=goods.goodsPrice * quantity,
                                     goodsName=goods.goodsName,
                                     goodsQuantity=quantity,
                                     customerName=customer.customerName,
                                     sellerName=seller[0].sellerName,
                                     shipTpAddress=ship_to_address,
                                     customerID=customer
                                     )
        return order.orderID
    except django.core.exceptions:
        # print('创建订单失败')
        return 0


def create_comment(customer_id, goods_id, comment_text):
    # 向数据库中插入一条评论
    try:
        customer = Customer.objects.get(customerID=customer_id)
        goods = Goods.objects.get(goodsID=goods_id)
        Comment.objects.create(
            goodsID=goods, customerID=customer, comment=comment_text)
        return True
    except django.core.exceptions:
        # print('添加评论失败')
        return False


# 登录


def customer_login_by_name(name, password):
    # 登陆成功返回id，否则返回0
    try:
        user = Customer.objects.get(customerName=name)
    except Customer.DoesNotExist:
        return 0
    else:
        if user.password == password:
            return user.customerID
        else:
            print('登录失败，密码错误')
            return 0


def customer_login_by_mail_address(mail_address, password):
    try:
        user = Customer.objects.get(mailAddress=mail_address)
    except Customer.DoesNotExist:
        return 0
    else:
        if user.password == password:
            return user.customerID
        else:
            return 0


def seller_login_by_mail_address(mail_address, password):
    try:
        user = Seller.objects.get(mailAddress=mail_address)
    except Seller.DoesNotExist:
        return 0
    else:
        if user.password == password:
            return user.sellerID
        else:
            print('登录失败，密码错误')
            return 0


def seller_login_by_name(name, password):
    try:
        user = Seller.objects.get(sellerName=name)
    except Seller.DoesNotExist:
        return 0
    else:
        if user.password == password:
            return user.sellerID
        else:
            print('登录失败，密码错误')
            return 0


# 商家管理方面


def show_goods_for_management(seller_id):
    # 返回列表seller_id对应的商品列表，按商品id排序
    # 返回QuerySet就行，暂时不考虑分页的问题
    try:
        goods_query_list = Goods.objects.filter(sellerID=seller_id).order_by('goodsID')  # 多对一的正向跨关系查询
    except django.core.exceptions:
        return 0
    else:
        return goods_query_list


def delete_goods(goods_id):
    # 下架商品
    try:
        goods = Goods.objects.get(goodsID=goods_id)
    except Goods.DoesNotExist:
        # print('goods_id_error:商品不存在')
        return
    else:
        goods.delete()

    # 用户管理方面


def show_intended_goods(customer_id):
    # 返回对应顾客的感兴趣商品列表
    try:
        intended_goods_querylist = IntendedGoods.objects.filter(customer__customerID=customer_id)
    except django.core.exceptions:
        return
    else:
        return intended_goods_querylist


def delete_intended_goods(customer_id, goods_id):
    try:
        intended_goods = IntendedGoods.objects.filter(goods__goodsID=goods_id, customer__customerID=customer_id)
    except django.core.exceptions:
        return
    else:
        intended_goods.get().delete()


def show_order(customer_id):
    try:
        order_query_set = Order.objects.filter(customer__customerID=customer_id).order_by('-orderID')
    except django.core.exceptions:
        return
    else:
        return order_query_set


def cancel_order(order_id):
    # 取消订单 返回True代表取消成功，返回False代表超时不可取消
    # Q:我觉得这里可以传一个以秒为单位的时间间隔，代表确认订单后多久时间内允许取消
    # A:但是，这样的话，就是以‘传参数’来确定订单能在多久时间取消了。
    # A:实际上订单多久内能够取消，应该和订单本身，或者商品本身有关。
    try:
        order = Order.objects.get(orderID=order_id)
    except Order.DoesNotExist:
        # print("order_id_error:订单不存在")
        return False
    else:
        if order.cancel():
            goods = Goods.objects.filter(seller__sellerName=order.sellerName).get(goodsName=order.goodsName)
            goods.goodsStock += order.goodsQuantity
            goods.goodsSold -= order.goodsQuantity
            goods.save()
            order.delete()
            return True
        else:
            return False
# 商品展示方面


def show_comment(goods_id):
    # 同样返回列表即可，按照时间反向排序
    try:
        comment_query_set = Comment.objects.filter(goodsID=goods_id).order_by('-commentID')
    except django.core.exceptions:
        return
    else:
        return comment_query_set


def comment(comment_id):
    # 删除对应评论
    try:
        obj = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return
    else:
        obj.delete()
    return


def get_search_list(keyword):
    try:
        search_list = Goods.objects.filter(goodsName__contains=keyword)
    except django.core.exceptions:
        return
    else:
        return search_list
