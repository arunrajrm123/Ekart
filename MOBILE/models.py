from django.db import models
from decimal import Decimal


class Uuser(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    repassword=models.CharField(max_length=255)
    phone_number=models.PositiveBigIntegerField(null=False, blank=False, default=1)
    blocked = models.BooleanField(default=False)
    def __str__(self) :
        return self.name
    def block_user(self):
        self.blocked = True
        self.save()
    def unblock_user(self):
        self.blocked = False
        self.save()
        
class Address(models.Model):
     user_id   =   models.ForeignKey(Uuser,on_delete=models.CASCADE, null=True)
     address_line=models.CharField(max_length=255)
     state=models.CharField(max_length=255)
     district=models.CharField(max_length=255)
     city=models.CharField(max_length=255)
     def __str__(self):
          return f"{self.address_line}, {self.city}, {self.district}, {self.state}"

class category(models.Model):
    name = models.CharField(max_length=100)
    descrition =  models.CharField(max_length=100)
    def __str__(self) :
        return self.name


class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    quantity= models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='product_images/')
    image2 = models.ImageField(upload_to='product_images1/')
    image3 = models.ImageField(upload_to='product_images2/')
    catogery=models.ForeignKey(category, on_delete=models.CASCADE)
    


class CartItem(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user       =   models.ForeignKey(Uuser,on_delete=models.CASCADE, null=True)
    product_id    =   models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity    =   models.IntegerField()
    def sub_total(self):
        return self.product_id.price * self.quantity
    def __str__(self):
        return self.product_id.name    


    
class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Out_for_delivery','Out_for_delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')
    )
    user_id = models.ForeignKey(Uuser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity= models.DecimalField(max_digits=10, decimal_places=1,null=True)
    status      =   models.CharField(max_length=30, choices=STATUS, default='Confirmed')
    is_cancelled = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    payment_method=models.CharField(max_length=255,null=True)
    def __str__(self):
        return f"Order ID: {self.id}"
    def cancel_order(self):
        self.is_cancelled = True
        self.save() 
    def return_order(self):
        self.is_returned = True
        self.save() 

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField()
    coupon_user = models.ForeignKey(Uuser, on_delete=models.CASCADE, null=True, blank=True)
    copuon_category = models.ForeignKey(category, on_delete=models.CASCADE, null=True, blank=True)
    referral_code = models.CharField(max_length=50, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    def apply_discount(self, amount):
        discount_amount = round(Decimal(self.discount) * amount)
        discounted_amount= amount - discount_amount
        return discounted_amount



class Wishlist(models.Model):
    wish_id = models.AutoField(primary_key=True)
    wish_user       =   models.ForeignKey(Uuser,on_delete=models.CASCADE, null=True)
    wish_product   =   models.ForeignKey(Product,on_delete=models.CASCADE)