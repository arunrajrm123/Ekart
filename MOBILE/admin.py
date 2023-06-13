from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(Wishlist)
admin.site.register(Uuser)
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(category)

