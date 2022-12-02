from . import models


def create_customer(customer_name, mail_address, password, phone_number):
    # 在数据库中创建一个customer，返回bool值， 创建成功则返回True， 创建失败(mail_address重复或customer重复)返回False
    return False


def create_seller(seller_name, mail_address, password, phone_number, shipping_address):
    # 在数据库中创建一个seller, 返回bool值， 成功返回True， 失败返回False, 同样，检测mail_address，seller_name的重复性
    return False


def create_goods(seller_id, goods_name, goods_stock, goods_price, goods_type):
    # 在数据库goods表，创建一个新的商品
    # 暂时先返回goods_id
    return 1


def create_photo_path(goods_id, photo_path):
    # 在数据库Photos表中，插入一个元组，成功创建返回True,失败则返回False
    return False


def create_intended_goods(customer_id, goods_id, quantity):
    # 意向商品表中插入一项
    # 不需要返回值
    return


def create_order(customer_id, goods_id, quantity, ship_to_address):
    # 订单表中创建一项order
    # amount, goodsName, customerName, sellerName,createTime 通过查找数据库计算得出
    return


def create_comment(customer_id, goods_id, comment):
    # 向数据库中插入一条评论
    return


def customer_login_by_name(name, password):
    # 返回布尔值
    return False


def customer_login_by_mail_address(mail_address, password):
    # 返回布尔值
    return False


def seller_login_by_mail_address(mail_address, password):
    # 返回布尔值
    return False


def seller_login_by_name(name, password):
    # 返回布尔值
    return False
