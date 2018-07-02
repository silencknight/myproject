from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11,null=True)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=1,null=True)
    pic = models.CharField(max_length=50,null=True)
    
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("show_users", "查看会员管理"),
            ("insert_users", "添加会员"),
            ("edit_users", "修改会员"),
            ("del_users", "删除会员")
        )

class Types(models.Model):
    typename = models.CharField(max_length=20) 
    pid = models.IntegerField()
    path = models.CharField(max_length=20)
    pic = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.typename

    class Meta:
        permissions = (
            ("show_types", "查看分类管理"),
            ("insert_types", "添加分类"),
            ("edit_types", "修改分类"),
            ("del_types", "删除分类")
        )


class Goods(models.Model):
    typeid = models.ForeignKey(to='Types',to_field='id')
    title = models.CharField(max_length=255)
    descr = models.CharField(max_length=255,null=True)
    info = models.TextField(null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    pic = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    store = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
    clicknum =models.IntegerField(default=0)
    addtime =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ("show_goods", "查看商品管理"),
            ("insert_goods", "添加商品"),
            ("edit_goods", "修改商品"),
            ("del_goods", "删除商品")
        )
    
class Address(models.Model):
    uid = models.ForeignKey(to="Users",to_field="id")
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=20)
    detail = models.CharField(max_length=50)
    status = models.IntegerField(default=0)

    class Meta:
        permissions = (
            ("show_address", "查看地址管理"),
            ("insert_address", "添加地址"),
            ("edit_address", "修改地址"),
            ("del_address", "删除地址")
        )

class Orders(models.Model):
    uid = models.ForeignKey(to="Users",to_field="id")
    addressid = models.ForeignKey(to="Address",to_field="id")
    tolprice = models.FloatField()
    tolnum = models.IntegerField()
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        permissions = (
            ("show_orders", "查看订单管理"),
            ("insert_orders", "添加订单"),
            ("edit_orders", "修改订单"),
            ("del_orders", "删除订单")
        )

class OrderInfo(models.Model):
    orderid = models.ForeignKey(to="Orders",to_field="id")
    gid = models.ForeignKey(to="Goods",to_field="id")
    num = models.IntegerField()
