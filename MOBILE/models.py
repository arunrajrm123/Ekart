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
    catewise_dicount_price=models.PositiveIntegerField(blank=True,null=True)
    def __str__(self) :
        return self.name

class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    catogery=models.ForeignKey(category, on_delete=models.CASCADE)
    
    
class Varient(models.Model):
    varient_name=models.CharField(max_length=100)
    product_key= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity= models.IntegerField()
    price = models.PositiveIntegerField(null=True)
    catogery_offer_price=models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='product_images/', null=True)
    image1 = models.ImageField(upload_to='product_images/', null=True)
    image2 = models.ImageField(upload_to='product_images/', null=True)


class CartItem(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user       =   models.ForeignKey(Uuser,on_delete=models.CASCADE, null=True)
    variant_id = models.ForeignKey(Varient, on_delete=models.CASCADE, null=True)
    quantity    =   models.IntegerField()
    def sub_total(self):
        if self.variant_id.catogery_offer_price==0:
           return self.variant_id.price * self.quantity
        else:
           return self.variant_id.catogery_offer_price * self.quantity 
    def __str__(self):
        return self. variant_id.product_key.name  


class Guest(models.Model):
    guest_id = models.AutoField(primary_key=True)
    guest_variant_id = models.ForeignKey(Varient, on_delete=models.CASCADE, null=True)
    guest_quantity    =   models.IntegerField()
    def sub_total(self):
        return self.guest_variant_id.price * self.guest_quantity
    def __str__(self):
        return self.guest_variant_id.product_key.name    


    
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
    varient_Key   =   models.ForeignKey(Varient, on_delete=models.CASCADE, null=True)
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
    coupon_dis_amount=models.PositiveIntegerField(default=100)
    coupon_minmun_amount=models.PositiveIntegerField(default=1000)
    coupon_user = models.ForeignKey(Uuser, on_delete=models.CASCADE, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    def apply_discount(self, amount):
        discount_amount = round(amount-Decimal(self.coupon_dis_amount)  )
        return discount_amount

class Couponapplied(models.Model):
    c_code=models.CharField(max_length=50,null=True, blank=True)
    c_user=models.ForeignKey(Uuser, on_delete=models.CASCADE, null=True, blank=True)


class Wishlist(models.Model):
    wish_id = models.AutoField(primary_key=True)
    wish_user       =   models.ForeignKey(Uuser,on_delete=models.CASCADE, null=True)
    wish_product   =   models.ForeignKey(Varient,on_delete=models.CASCADE)


class Wallet(models.Model):
    w_user=models.ForeignKey(Uuser,on_delete=models.CASCADE, null=True)
    amount=models.PositiveIntegerField()