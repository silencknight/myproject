from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=1,null=True)
    pic = models.CharField(max_length=50,null=True)
    
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)




class Types(models.Model):
    typename = models.CharField(max_length=20,unique=True) 
    pid = models.IntegerField()
    path = models.CharField(max_length=20)


# class Goods(models.Model):
#     typeid = models.ForeignKey(to='Types',to_field='id')
#     title = models.CharField(max_length=50)
#     descr = models.CharField(max_length=100)
#     price = models.IntegerField(max_digits=10,decimal_place=2)
#     pic = models.CharField(max_length=80)
#     status = models.IntegerField(default=0)
#     store = models.IntegerField(default=0)
#     num = models.IntegerField(default=0)
#     clicknum =models.IntegerField(default=0)
#     addtime =models.DateTimeField(auto_now_add=True)
#     
