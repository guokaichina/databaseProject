# Generated by Django 4.1.3 on 2022-12-10 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NetworkingMall', '0005_alter_order_customername_alter_order_sellername'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='goodsName',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]
