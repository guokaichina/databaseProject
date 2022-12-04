from .models import *


def create_customer(customer_name, mail_address, password, phone_number):
    # 在数据库中创建一个customer，返回bool值， 创建成功则返回True， 创建失败(mail_address重复或customer重复)返回False  
    try:
        customer_set_1 = Customer.objects.filter(customerName=customer_name)
        customer_set_2 = Customer.objects.filter(mailAddress=mail_address)

        if customer_set_1.exists() and customer_set_2.exists():
            '''print('用户名已被占用; 邮箱已注册账号')'''
            return False
        elif customer_set_1.exists():
            '''print('用户名已被占用')'''
            return False
        elif customer_set_2.exists():
            '''print('邮箱已注册账号')'''
            return False
        else:
            Customer.objects.create(customerName=customer_name, mailAddress=mail_address,
                                    password=password, phoneNumber=phone_number)
            return True
    except:
        print('创建顾客用户异常')
        return False


def create_seller(seller_name, mail_address, password, phone_number, shipping_address):
    # 在数据库中创建一个seller, 返回bool值， 成功返回True， 用户名重复、邮箱重复或创建失败返回False 同样，检测mail_address，seller_name的重复性
    try:
        seller_set_1 = Seller.objects.filter(sellerName=seller_name)
        seller_set_2 = Seller.objects.filter(mailAddress=mail_address)

        if seller_set_1.exists() and seller_set_2.exists():
            '''print('用户名已被占用; 邮箱已注册账号')'''
            return False
        elif seller_set_1.exists():
            '''print('用户名已被占用')'''
            return False
        elif seller_set_2.exists():
            '''print('邮箱已注册账号')'''
            return False
        else:
            Seller.objects.create(sellerName=seller_name, mailAddress=mail_address,
                                  password=password, phoneNumber=phone_number, shippingAddress=shipping_address)
            return True
    except:
        print('创建商家用户异常')
        return False


def create_goods(seller_id, goods_name, goods_stock, goods_price, goods_type):
    # 在数据库goods表，创建一个新的商品,创建成功返回goodsID，创建失败返回0
    # 暂时先返回goods_id
    try:
        seller = Seller.objects.get(sellerID=seller_id)
        goods = Goods.objects.create(goodsName=goods_name, goodsStock=goods_stock, goodsPrice=goods_price,
                                     goodsType=goods_type, sellerID=seller)
        return goods.goodsID
    except Seller.DoesNotExist:
        print('seller_id_error:商家不存在')
    except:
        print('create_goods_error:添加新商品失败')  # 创建商品失败
        return 0


def create_photo_path(goods_id, photo_path):
    # 在数据库Photos表中，插入一个元组，成功创建返回True,失败则返回False
    try:
        goods = Goods.objects.get(goodsID=goods_id)
        Photos.objects.create(goodsID=goods, photosPath=photo_path)
    except Goods.DoesNotExist:
        print('goods_id_error:商品不存在')
        return False
    except:
        return False


def create_intended_goods(customer_id, goods_id, quantity):
    # 意向商品表中插入一项 不需要返回值
    try:
        customer = Customer.objects.get(customerID=customer_id)
        goods = Goods.objects.get(goodsID=goods_id)
        IntendedGoods.objects.create(goodsID=goods, customerID=customer, quantity=quantity)
    except Customer.DoesNotExist:
        print('customer_id_error:顾客不存在')
    except Goods.DoesNotExist:
        print('goods_id_error:商品不存在')
    except:
        print('添加意向商品失败')


def create_order(customer_id, goods_id, quantity, ship_to_address):
    # 订单表中创建一项order
    # amount, goodsName, customerName, sellerName,createTime 通过查找数据库计算得出
    try:
        customer = Customer.objects.get(customerID=customer_id)
        goods = Goods.objects.get(goodsID=goods_id)
        seller = Seller.objects.filter(goods__goodsID=goods_id)

        Order.objects.create(amount=goods.goodsPrice * quantity,
                             goodsName=goods.goodsName,
                             goodsQuantity=quantity,
                             customerName=customer.customerName,
                             sellerName=seller[0].sellerName,
                             shipTpAddress=ship_to_address,
                             customerID=customer
                             )
    except Customer.DoesNotExist:
        print('customer_id_error:顾客不存在')
    except Goods.DoesNotExist:
        print('goods_id_error:商品不存在')
    except:
        print('创建订单失败')


def create_comment(customer_id, goods_id, comment):
    # 向数据库中插入一条评论
    try:
        customer = Customer.objects.get(customerID=customer_id)
        goods = Goods.objects.get(goodsID=goods_id)
        Comment.objects.create(goodsID=goods, customerID=customer, comment=comment)
    except Customer.DoesNotExist:
        print('customer_id_error:顾客不存在')
    except Goods.DoesNotExist:
        print('goods_id_error:商品不存在')
    except:
        print('添加评论失败')


def customer_login_by_name(name, password):
    # 登陆成功返回id，否则返回0
    user = Customer.objects.get(customerName=name)
    if user is None:
        print('登录失败，用户名不存在')
        return 0
    else:
        if user.password == password:
            return user.customerID
        else:
            print('登录失败，密码错误')
            return 0


def customer_login_by_mail_address(mail_address, password):
    user = Customer.objects.get(mailAddress=mail_address)
    if user is None:
        print('登录失败，用户邮箱不存在')
        return 0
    else:
        if user.password == password:
            return user.customerID
        else:
            print('登录失败，密码错误')
            return 0


def seller_login_by_mail_address(mail_address, password):
    user = Seller.objects.get(mailAddress=mail_address)
    if user is None:
        print('登录失败，用户邮箱不存在')
        return 0
    else:
        if user.password == password:
            return user.get().sellerID
        else:
            print('登录失败，密码错误')
            return 0


def seller_login_by_name(name, password):
    user = Seller.objects.get(sellerName=name)
    if user is None:
        print('登录失败，用户名不存在')
        return 0
    else:
        if user.password == password:
            return user.get().sellerID
        else:
            print('登录失败，密码错误')
            return 0
