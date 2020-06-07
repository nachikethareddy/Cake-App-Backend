from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone


class CakeShopDetails(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=255)
    branch_address = models.TextField(default='No Address!')


class CakeDepartment(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    cake_shop = models.ForeignKey(CakeShopDetails,on_delete=models.CASCADE)
    department_name = models.CharField(max_length=200)
    department_image = models.FileField(upload_to='cake_departments/')


class Cakes(models.Model):
    id =models.UUIDField(default=uuid.uuid4,primary_key=True)
    cake_name = models.CharField(max_length=255)
    cake_department = models.ForeignKey(CakeDepartment,on_delete=models.CASCADE)
    cake_image = models.FileField(upload_to='cake_images/')
    half_kg_available = models.BooleanField(default=True)
    maximum_kgs= models.IntegerField(default=10)
    half_kg_price = models.IntegerField(default=0)
    one_kg_price = models.IntegerField(default=0)
    egg_less_price = models.IntegerField(default=50)
    is_egless_available = models.BooleanField(default=True)
    is_totally_eggless_cake = models.BooleanField(default=False)
    custom_photo_upload = models.BooleanField(default=False)
    does_this_have_flavours = models.BooleanField(default=False)


class FlavourRoot(models.Model):
    id =models.UUIDField(default=uuid.uuid4,primary_key=True)
    falvour_root = models.CharField(max_length=255)

class Flavors(models.Model):
    id =models.UUIDField(default=uuid.uuid4,primary_key=True)
    falvour_name = models.CharField(max_length=255)
    falvour_root = models.ForeignKey(FlavourRoot,on_delete=models.CASCADE)
    cake = models.ForeignKey(Cakes,on_delete=models.CASCADE)
    half_kg_available = models.BooleanField(default=True)
    maximum_kgs= models.IntegerField(default=10)
    half_kg_price = models.IntegerField(default=0)
    one_kg_price = models.IntegerField(default=0)
    egg_less_price = models.IntegerField(default=50)
    is_egless_available = models.BooleanField(default=True)


class UserCakeShopRelationship(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    cake_shop = models.ForeignKey(CakeShopDetails,on_delete=models.CASCADE)


class UserOccasion(models.Model):
    id = models.AutoField(auto_created = True,primary_key = True)
    phone = models.CharField(max_length=20)
    occasion = models.CharField(max_length=100)

class OrderCake(models.Model):
    id = models.AutoField(auto_created = True,primary_key = True)
    name = models.CharField(max_length=255)
    cake_details = models.ForeignKey(Cakes,on_delete=models.CASCADE)
    flavor = models.ForeignKey(Flavors,on_delete=models.CASCADE,null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True)
    date_of_order = models.DateTimeField(auto_now=True,editable=False)
    occasion_root = models.ForeignKey(UserOccasion,on_delete=models.CASCADE)
    date_of_delivery = models.DateTimeField()
    message_on_cake = models.CharField(max_length=255)
    special_instructions = models.CharField(max_length=255)
    eggless =models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    weight = models.DecimalField(default=0.5,max_digits=5, decimal_places=2)



class PhotoCakeLogger(models.Model):
    order = models.OneToOneField(OrderCake,on_delete=models.CASCADE)
    photo = models.FileField(upload_to='cake_order_photos/')