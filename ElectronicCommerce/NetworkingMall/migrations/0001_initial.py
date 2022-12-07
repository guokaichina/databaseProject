# Generated by Django 4.1.3 on 2022-12-07 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentID', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=100)),
                ('commentTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['goodsID', '-commentTime'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customerID', models.AutoField(primary_key=True, serialize=False)),
                ('mailAddress', models.EmailField(max_length=254, unique=True)),
                ('customerName', models.CharField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('phoneNumber', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('goodsID', models.AutoField(primary_key=True, serialize=False)),
                ('goodsName', models.CharField(max_length=60)),
                ('goodsStock', models.IntegerField()),
                ('goodsSold', models.IntegerField()),
                ('goodsPrice', models.DecimalField(decimal_places=2, max_digits=12)),
                ('goodsType', models.CharField(choices=[('1', '女装'), ('2', '男装'), ('3', '食品'), ('4', '医药'), ('5', '洗护'), ('6', '饰品'), ('7', '百货'), ('8', '内衣'), ('9', '运动'), ('10', '企业'), ('11', '进口'), ('12', '母婴'), ('13', '手机'), ('14', '鞋靴'), ('15', '数码'), ('16', '箱包'), ('17', '电器'), ('18', '美妆'), ('19', '图书'), ('20', '家装'), ('21', '保健'), ('22', '车品'), ('23', '生鲜'), ('24', '奢品')], max_length=20)),
                ('commentedCustomer', models.ManyToManyField(through='NetworkingMall.Comment', to='NetworkingMall.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('sellerID', models.AutoField(primary_key=True, serialize=False)),
                ('mailAddress', models.EmailField(max_length=254, unique=True)),
                ('sellerName', models.CharField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('phoneNumber', models.CharField(max_length=20)),
                ('shippingAddress', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('photoID', models.AutoField(primary_key=True, serialize=False)),
                ('photoPath', models.CharField(max_length=10, unique=True)),
                ('goodsID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NetworkingMall.goods')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderID', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('goodsName', models.CharField(max_length=60)),
                ('goodsQuantity', models.IntegerField()),
                ('customerName', models.CharField(max_length=40, unique=True)),
                ('sellerName', models.CharField(max_length=40, unique=True)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('shipToAddress', models.CharField(max_length=80)),
                ('customerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NetworkingMall.customer')),
            ],
        ),
        migrations.CreateModel(
            name='IntendedGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('customerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NetworkingMall.customer')),
                ('goodsID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NetworkingMall.goods')),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='sellerID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NetworkingMall.seller'),
        ),
        migrations.AddField(
            model_name='comment',
            name='customerID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NetworkingMall.customer'),
        ),
        migrations.AddField(
            model_name='comment',
            name='goodsID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NetworkingMall.goods'),
        ),
    ]
