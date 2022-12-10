import datetime
from django.db import models


# 顾客信息模型
class Customer(models.Model):
    # 主键 顾客用户ID IntegerField, 可以根据可用的ID自动递增
    customerID = models.AutoField(primary_key=True)
    # 邮件地址 CharField 使用EmailValidator来检查该值是否是有效的邮件地址
    mailAddress = models.EmailField(unique=True)
    customerName = models.CharField(max_length=40, unique=True)  # 顾客用户名
    password = models.CharField(max_length=20)  # 密码
    phoneNumber = models.CharField(max_length=20)  # 手机号

    def __str__(self):
        return "顾客ID:{} {} {} 密码:{} 手机号:{}".format(self.customerID,  self.customerName, self.mailAddress,
                                                   self.password, self.phoneNumber)


# 商家信息模型
class Seller(models.Model):

    sellerID = models.AutoField(primary_key=True)  # 主键 商家用户ID IntegerField
    mailAddress = models.EmailField(unique=True)  # 邮件地址 CharField
    sellerName = models.CharField(max_length=40, unique=True)  # 商家用户名
    password = models.CharField(max_length=20)  # 密码
    phoneNumber = models.CharField(max_length=20)  # 手机号
    shippingAddress = models.CharField(max_length=80)  # 发货地址

    def __str__(self):
        return "商家ID:{} {} {} 密码:{} 手机号:{} {}".format(self.sellerID, self.sellerName, self.mailAddress,
                                                      self.password, self.phoneNumber, self.shippingAddress)


# 商品信息模型
class Goods(models.Model):

    goodtype = [
        ('1', '女装'), ('2', '男装'), ('3', '食品'), ('4', '医药'), ('5', '日用'), ('6', '饰品'),
        ('7', '运动'), ('8', '电子'), ('9', '图书'), ('10', '其它'),
    ]

    goodsID = models.AutoField(primary_key=True)  # 主键 商品ID IntegerField
    goodsName = models.CharField(max_length=60)  # 商品名
    goodsStock = models.IntegerField()  # 商品库存量
    goodsSold = models.IntegerField()  # 商品销量
    goodsPrice = models.DecimalField(
        max_digits=12, decimal_places=2)  # 商品价格 使用TextInput表单部件
    # 以两位小数的精度来存储整数位有10位的数字 ； 以DecimalValidator来验证输入是否是固定精度的十进制
    goodsType = models.CharField(max_length=20, choices=goodtype)  # 商品种类
    # 在表单中以选择框的形式呈现
    # sellerID仍需更完善的定义
    sellerID = models.ForeignKey(
        'Seller',
        on_delete=models.CASCADE,
    )   # 外码 商家ID 商家和商品之间是一对多关系
    commentedCustomer = models.ManyToManyField(
        Customer, through='Comment')  # 商品和顾客之间通过中间模型Comment关联起来

    def __str__(self):
        return "商品ID:{} {} 库存{}件 {}RMB {} 卖家ID:{}".format(self.goodsID, self.goodsName, self.goodsStock,
                                                          self.goodsPrice, self.goodsType, self.sellerID)


# 商品照片模型
class Photo(models.Model):

    photoID = models.AutoField(primary_key=True)  # 主码 图片ID
    photoPath = models.CharField(max_length=10, unique=True, null=False)  # 图片名
    # goodsID仍需更完善的定义
    goodsID = models.ForeignKey(
        'Goods',
        on_delete=models.CASCADE,
    )   # 外码 商品ID 商家和图片之间是一对多关系

    def __str__(self):
        return "照片ID:{} {} 商品ID:{}".format(self.photoID, self.photoPath, self.goodsID)


# 意向商品模型
class IntendedGoods(models.Model):
    goodsID = models.ForeignKey(
        'Goods',
        on_delete=models.CASCADE,
    )  # 外码 商品ID
    quantity = models.IntegerField()  # 商品数量
    customerID = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
    )  # 外码 顾客ID 顾客和意向商品之间是一对多关系

    def __str__(self):
        return "顾客ID{} 商品ID:{} {}件".format(self.customerID, self.goodsID, self.quantity)


# 订单信息模型
class Order(models.Model):
    orderID = models.AutoField(primary_key=True)  # 主码 订单号
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # 订单价格
    goodsName = models.CharField(max_length=60)  # 商品名
    goodsQuantity = models.IntegerField()  # 商品数量
    customerName = models.CharField(max_length=40)  # 顾客用户名
    sellerName = models.CharField(max_length=40)  # 商家用户名
    createTime = models.DateTimeField(
        auto_now=False, auto_now_add=True)  # 创建时间
    shipToAddress = models.CharField(max_length=80)  # 收货地址
    receivingStatus = models.BooleanField(default=False)  # 收货状态 True为已收货， False为未收货
    customerID = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
    )  # 外码 顾客ID

    def __str__(self):
        return "订单ID:{} {}RMB {} {}件 顾客:{} 商家:{} {} 收货地址{}".format(self.orderID, self.amount, self.goodsName,
                                                                   self.goodsQuantity, self.customerName,
                                                                   self.sellerName, self.createTime, self.shipToAddress)

    # 判断此订单在某一时间间隔内是否可以取消
    def cancel(self, interval=4320):  # 默认三天内可取消,以秒为单位
        now_time = datetime.datetime.now()
        create_time = datetime.datetime.strptime(
            self.createTime.__str__(), "%Y-%m-%d %H:%M:%S")
        if (now_time-create_time).total_seconds() <= interval:
            return True
        else:
            return False


# 评论模型
class Comment(models.Model):

    commentID = models.AutoField(primary_key=True)  # 评论ID
    customerID = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
    )  # 外码 顾客ID
    goodsID = models.ForeignKey(
        'Goods',
        on_delete=models.CASCADE,
    )  # 外码 商品ID
    comment = models.CharField(max_length=100)  # 评论内容
    commentTime = models.DateTimeField(auto_now=False, auto_now_add=True)  # 评论时间

    def __str__(self):
        return "顾客ID:{} 商品ID:{} {} {}".format(self.customerID, self.goodsID, self.comment, self.commentTime)

    class Meta:
        ordering = ["goodsID", "-commentTime"]  # 默认先按ID升排，再按时间降排
