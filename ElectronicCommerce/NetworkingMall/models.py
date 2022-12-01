import os
import datetime
from django.conf import settings
from django.db import models

# 1.编写后端希望的接口
#    
# 2.整理重构Django已有的接口

'''接口函数文档(包含自定义API与Django API)'''
# 1.创建对象/在表中insert新行
#   创建对象，使用关键字参数初始化对象，调用对象的save()方法将其存入数据表
#   等同于 obj = modelsClass.object.create(关键字参数列表) ，此方法将创建于保存对象一步到位
# 2.修改对象/在表中update某一行
#   2.1修改字段值，调用对象的save()函数保存
#   2.2修改ForeignKey或MangToManyField
#       2.2.1 ForeignKey为一对多关系，没有关系表。
#               更新方法：类似修改普通字段值，赋值后，调用save()保存即可
#       2.2.2 MangToMany为多对多关系，存在关系表。
#               更新方法：向多对多关系表中添加记录时，首先初始化多对多关系中没有ManyToMany字段M的对象A，
#                        然后多对多关系中有ManyToMany字段M的对象B，调用B.M.add(A1,A2,..,An),便向多对多关系表中添加了记录（实际应该是将记录添加到了中间模型中）
# 3.检索对象/在表中查询满足条件的记录






def images_path():
    return os.path.join(settings.LOCAL_FILE_DIR, 'image') #需要重写

# 顾客信息模型
class Customer(models.Model):
    
    customerID = models.AutoField(primary_key=True) # 主键 顾客用户ID IntegerField, 可以根据可用的ID自动递增
    mailAddress = models.EmailField() # 邮件地址 CharField 使用EmailValidator来检查该值是否是有效的邮件地址
    customerName = models.CharField(max_length=40, unique=True) # 顾客用户名
    password = models.CharField(max_length=20) # 密码
    phoneNumber= models.CharField(max_length=20) # 手机号

    def __str__(self):
        return "{} {} {} {} {}".format(self.customerID, self.mailAddress, self.customerName, self.password, self.phoneNumber)

# 商家信息模型
class Seller(models.Model):
    
    sellerID = models.AutoField(primary_key=True) # 主键 商家用户ID IntegerField
    mailAddress = models.EmailField() # 邮件地址 CharField 
    sellerName = models.CharField(max_length=40, unique=True) # 商家用户名
    password = models.CharField(max_length=20) # 密码
    phoneNumber = models.CharField(max_length=20) # 手机号
    shippingAddress = models.CharField(max_length=80) # 发货地址

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.sellerID, self.mailAddress, self.sellerName, self.password, self.phoneNumber, self.shippingAddress)


# 商品信息模型
class Goods(models.Model):
    
    goodtype = [
        ('1','女装'),('2','男装'),('3','食品'),('4','医药'), #后期根据需求再添加选项
    ]
    
    goodsID = models.AutoField(primary_key=True) # 主键 商品ID IntegerField
    goodsName = models.CharField(max_length=60) # 商品名
    goodsStock = models.IntegerField() # 商品库存量
    goodsPrice = models.DecimalField(max_digits=12, decimal_places=2) # 商品价格 使用NumberInput表单部件
    # 以两位小数的精度来存储整数位有10位的数字 ； 以DecimalValidator来验证输入是否是固定精度的十进制
    goodsType = models.CharField(max_length=20, choices = goodtype) # 商品种类
    # 在表单中以选择框的形式呈现
    #sellerID仍需更完善的定义
    sellerID = models.ForeignKey(
        'Seller',
        on_delete=models.CASCADE,
        )   # 外码 商家ID 商家和商品之间是一对多关系
    commentedCustomer = models.ManyToManyField(Customer, through='Comment') # 商品和顾客之间通过中间模型Comment关联起来

    def __str__(self):
        return "{} {} 库存{}件 {}RMB {} {} 卖家ID:{}".format(self.goodsID, self.goodsName, 
                            self.goodsStock, self.goodsPrice, self.goodsType, self.sellerID)


# 商品照片模型
class Photos(models.Model):
    
    photosID = models.AutoField(primary_key=True) # 主码 图片ID
    photosPath = models.FilePathField(path=images_path, unique=True) # 图片路径
    #goodsID仍需更完善的定义
    goodsID = models.ForeignKey(
        'Goods',
        on_delete=models.CASCADE,
        )   # 外码 商品ID 商家和图片之间是一对多关系

    def __str__(self):
        return "{} {} 商品ID{}".format(self.photosID, self.photosPath, self.goodsID)

# 意向商品模型 
class IntendedGoods(models.Model):
    goodsID = models.ForeignKey(
        'Goods',
        on_delete=models.CASCADE,
    ) # 外码 商品ID
    quantity = models.IntegerField() # 商品数量
    customerID = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
    ) # 外码 顾客ID 顾客和意向商品之间是一对多关系

    def __str__(self):
        return "顾客ID{} 商品ID{} {}件".format(self.customerID, self.goodsID, self.quantity)


# 订单信息模型
class Order(models.Model):
    orderID = models.AutoField(primary_key=True) # 主码 商品ID
    amount = models.DecimalField(max_digits=12, decimal_places=2) # 订单价格
    goodsName = models.CharField(max_length=60) # 商品名
    goodsQuantity = models.IntegerField() # 商品数量
    customerName = models.CharField(max_length = 40, unique=True) # 顾客用户名
    sellerName = models.CharField(max_length=40, unique=True) # 商家用户名
    createTime = models.DateTimeField(auto_now=False, auto_now_add=True) # 创建时间
    shipToAddress = models.CharField(max_length=80) # 收货地址
    customerID = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
    ) # 外码 顾客ID

    def __str__(self):
        return "商品ID{} {}RMB {} {}件 顾客:{} 商家:{} {} 收货地址{}".format(self.orderID, self.amount, self.goodsName, self.goodsQuantity, 
        self.customerName, self.sellerName, self.createTime, self.shipToAddress)
    
    # 判断此订单在某一时间间隔内是否可以取消
    def cancel(self, interval = 4320): # 默认三天内可取消
        nowtime = datetime.datetime.now()
        createTime = datetime.strptime(self.createTime, "%Y-%m-%d %H:%M:%S")

        if (nowtime-createTime).total_seconds <= interval:
            return True
        else:
            return False



# 评论模型 （中间模型）
class Comment(models.Model):
    customerID = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
    ) #外码  顾客用户ID
    goodsID = models.ForeignKey(
        'Goods',
        on_delete=models.CASCADE,
    ) #外码 商品ID
    comment = models.CharField(max_length=100) # 评论内容

    def __str__(self):
        return "{} {} {}".format(self.customerID, self.goodsID, self.comment)
