from django.shortcuts import render,redirect
from. models import*
from django.shortcuts import render,redirect,HttpResponse
import re
import requests, random
import os
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import *
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
import pyotp
from .models import Product, category
from django.shortcuts import render, redirect
import razorpay
from .models import*
import vonage
client = vonage.Client(key="49f664eb", secret="fFe4DCMVuzhsv1pr")
sms = vonage.Sms(client)
# Create your views here.
@never_cache
def registerform(request):
    if "password" in request.session:
        redirect("admin_home.html")
    if 'name' in request.session:
        return render(request, 'home.html')
    # if request.user.is_authenticated:
    #  return redirect('admin_home')
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        phone_number = request.POST.get('phone_number')
        print(phone_number)
        error = None
        if(not name):
         error='name is required'
        if name:
            if len(name)<4:
             error='Name must longer than 4' 
        if not name.isalpha():
            error='alphabets only'
        if len(password)<4:
            error='password should contain 4 characters or numbers '   
        if password!=repassword:
            error='password is incorrect' 
        if not re.match (r'^[\w-]+(\.[\w-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,})$',email):
            error='enter valid email address'
        if phone_number is not None:
            if len(phone_number) < 10:
                error = 'phone_number should contain 10 characters or numbers '
        if not error:
            print(name,password,email,repassword,phone_number)
        else:   
         return render(request,'signup.html',{'error':error}) 
        if not error:
            # Generate a random 6-digit OTP
            otp = str(random.randint(100000, 999999))
            # Send the SMS using Vonage
            responseData = sms.send_message(
                {
                    "from": "Vonage APIs",
                    "to": "+919746593526",
                    "text": f"Your OTP is: {otp}",
                }
            )
            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")
            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
            # Save the OTP and other details in the Uuser model
            form = Uuser(name=name, email=email, password=password, repassword=repassword,
                         phone_number=phone_number)
            form.save()
            print(otp)
            return redirect('verify_otp', otp=otp)
    else:
        return render(request, 'signup.html')

@never_cache
def otp_grn(request, otp):
    if request.method == 'POST':
        if request.POST.get('otp') == otp:
            # OTP is valid, redirect to another page
            return render(request, 'home.html')
        else:
            # OTP is invalid, render the OTP verification page again with an error message
            msg = 'Enter valid OTP'
            return render(request, 'otp.html', {'msg': msg})
    else:
        # Render the OTP verification page
        return render(request, 'otp.html')
@never_cache
def loginn(request):
    if 'name' in request.session:
        return render(request, 'home.html')
    if "password" in request.session:
        return redirect('admin_home')
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        users = Uuser.objects.filter(name=name, password=password)
        if users.exists():
            users = users.first()
            if users.blocked:
                dict = 'Your account is blocked. Please contact the administrator.'
                return render(request, 'logging.html', {'dict': dict})
            request.session["name"] = name
            return render(request, 'home.html')
        else:
            dict = 'Invalid name or password'
            return render(request, 'logging.html', {'dict': dict})
    else:
        return render(request, 'logging.html')   

@never_cache
def home(request):
  if "password" in request.session:
        return redirect('admin_home')
  
  if "name" in request.session:
    return render(request,'home.html')
  else:
        return redirect(index)

@never_cache

def user_logout(request):
    if "name" in request.session:
      del request.session['name']      
      return render(request,"index.html")
    else:
      return redirect(index)
@never_cache
def index(request):
   if "password" in request.session:
        return redirect('admin_home')
   if 'name' in request.session:
        return render(request, 'home.html')
   if "password" in request.session:
      return redirect(admin_home)
   return render(request,'index.html')

@never_cache
def admin_login(request):
  if "password" in request.session:
    return render(request, 'admin_home.html')
  elif request.method == 'GET':
    return render(request, 'admin_login.html')
  else:
      if request.method == 'POST':
          name = request.POST.get('username')
          password = request.POST.get('password')
          user = authenticate(request, username=name, password=password)
          if user is not None:
              request.session["password"] = password
              
              return render(request,'admin_home.html')
          else:
              dict= 'invalid Name or password..!'
  return render(request, 'admin_login.html',{'dict':dict})



@never_cache
def admin_home(request):
    if "password" in request.session:
      return render(request,"admin_home.html")
    else:
       return render(request,"admin_login.html")
@never_cache
def admin_logout(request):
  if "password" in request.session:
    del request.session['password']
    return render(request,'admin_login.html')
  else:
      return render(request,'admin_login.html')
@never_cache 
def user_list(request):
    if "password" in request.session:
        search = request.GET.get('search')
        if search:
            users = Uuser.objects.filter(name__istartswith=search)
        else:
            users = Uuser.objects.all()
        
        # Add block/unblock functionality
        action = request.GET.get('action')
        if action == 'block':
            user_id = request.GET.get('id')
            users = Uuser.objects.get(id=user_id)
            users.block_user()
        elif action == 'unblock':
            user_id = request.GET.get('id')
            users = Uuser.objects.get(id=user_id)
            users.unblock_user()
        
        return render(request, 'userlist.html', {'users':users})
    else:
        return redirect('admin_login')
    


@never_cache
def block_user(request, id):
    users = get_object_or_404(Uuser, id=id)
    users.block_user()
    return redirect('userlist')

@never_cache
def unblock_user(request, id):
    users = get_object_or_404(Uuser, id=id)
    users.unblock_user()
    return redirect('userlist')



@never_cache
def view_category(request):
    if "password" in request.session:
        search = request.GET.get('search')
        if search:
            cato = category.objects.filter(name__istartswith=search)
        else:
            cato = category.objects.all()
        return render(request, 'view_catogery.html', {'cato': cato})
    else:
        return redirect('admin_login')



@never_cache
def add_catogery(request):
   
    if request.method == 'POST':
        name = request.POST.get('name')
        descrition= request.POST.get('descrition')
        # Retrieve the category object based on the submitted name
        

        # Create the Product object with the correct category ID
        cato = category.objects.create(
            name=name,
           descrition=descrition
        )
       
        return redirect(view_category)

    return render(request, 'add_catogery.html')


@never_cache

def edit_category(request,id):
    cato = get_object_or_404(category, id=id)

    if request.method == 'POST':
        cato.name = request.POST.get('name')
       
        cato.descrition= request.POST.get('descrition')

        cato.save()
        return redirect('viewcatogery')
    else:
        context = {'cato': cato}
        return render(request, 'edit_catogery.html', context)
    


@never_cache
def delete_category(request,id):
   
   cato=category.objects.get(id=id)
   cato.delete()
   return redirect(view_category) 


@never_cache
def product_view(request):
    if "password" in request.session:
        search = request.GET.get('search')
        if search:
            products = Product.objects.filter(name__istartswith=search)
        else:
            products = Product.objects.all()
        
        return render(request, 'product_view.html', {'products': products})
    else:
        return redirect('admin_login')

@never_cache
def add_product(request):
   if "password" in request.session:
    if request.method == 'POST':
        name = request.POST.get('name')
        catogery_name = request.POST.get('catogery')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        catogery = category.objects.get(name=catogery_name)
        # Create the Product object with the correct category ID
        product = Product.objects.create(
            name=name,
            catogery=catogery,
            description=description,
            quantity=quantity,
            price=price,
            image1=image1,
            image2=image2,
            image3=image3
        )
        product.save()
        return redirect(product_view)
    return render(request, 'add.html')
   else:
    return redirect('admin_login')
       


@never_cache
def edit(request, product_id):
    prod = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        prod.name = request.POST.get('name')
        prod.description = request.POST.get('description')
        prod.price = request.POST.get('price')
        prod.quantity = request.POST.get('quantity')

        # Check if new images are provided
        if 'image1' in request.FILES:
            # Delete the existing image1 file
            if prod.image1:
                os.remove(prod.image1.path)
            prod.image1 = request.FILES.get('image1')

        if 'image2' in request.FILES:
            # Delete the existing image2 file
            if prod.image2:
                os.remove(prod.image2.path)
            prod.image2 = request.FILES.get('image2')

        if 'image3' in request.FILES:
            # Delete the existing image3 file
            if prod.image3:
                os.remove(prod.image3.path)
            prod.image3 = request.FILES.get('image3')

        category_name = request.POST.get('category')

        # Retrieve the category if it exists, otherwise create a new category
        cat_obj, _ = category.objects.get_or_create(name=category_name)
        prod.category = cat_obj

        prod.save()
        return redirect('productview')
    else:
        context = {'prod': prod}
        return render(request, 'edit.html', context)



@never_cache
def delete_product(request, product_id):
   product=Product.objects.get(product_id=product_id)
   product.delete()
   return redirect(product_view) 


# def home_2(request):
#     return render(request,'home-03.html')


def shop(request):
    if "password" in request.session:
        return redirect('admin_home')
    else:
        
            search = request.GET.get('search')
            category_filter = request.GET.get('name')
            price_range_filter = request.GET.get('price_range')

            # Filter products based on search query
            if search:
                products = Product.objects.filter(name__istartswith=search)
            else:
                products = Product.objects.all()

            # Apply category filter
            if category_filter:
                catogery=category.objects.get(name=category_filter)
                products = products.filter(catogery=catogery.id)

            # Apply price range filter
            if price_range_filter:
                min_price, max_price = price_range_filter.split('-')
                products = products.filter(price__gte=min_price, price__lte=max_price)
            if request.method == 'POST':
            # Retrieve the product ID from the POST data
                product_id = request.POST.get('product_id')

                # Retrieve the product based on the product ID
                
                product = get_object_or_404(Product, product_id=product_id)

                if 'name' in request.session:
                    # Retrieve the user's name from the session
                    user_name = request.session['name']

                    # Retrieve the user based on the name
                    users = get_object_or_404(Uuser, name=user_name)

                    # Check if the cart item already exists for the user and the product
                    wish_item = Wishlist.objects.filter(wish_user=users, wish_product=product).first()

                    if wish_item:                  # If the cart item already exists, update its quantity
                     messages.info(request, 'This item is already in your cart.')
                    
                    else:
                        # If the cart item doesn't exist, create a new one
                        wish_item =Wishlist(wish_user=users, wish_product=product)

                    # Save the cart item
                    wish_item.save()
                

            return render(request, 'shop.html', {'products': products,'products': products})
    
   
@never_cache
def wishlist(request):
    if "password" in request.session:
        return redirect('admin_home')
    if 'name' in request.session:
        user_name = request.session['name']
        user = get_object_or_404(Uuser, name=user_name)
        wish_items = Wishlist.objects.filter(wish_user=user)
        product=None
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            # Handle form submission
            product = Product.objects.get(product_id=product_id)
            wishlist_item = Wishlist(wish_user=user, wish_product=product)
            wishlist_item.save()
        
            
        return render(request, 'wishlist.html', {'wish_items': wish_items, 'product': product})
    else:
        return redirect('loginn')



@never_cache
def wish_add_cart(request):
            if "password" in request.session:
                 return redirect('admin_home')
            produ = request.POST.get('prod')
            product = get_object_or_404(Product, product_id=produ)

            if product.quantity > 0:
                if 'name' in request.session:
                    # Retrieve the user's name from the session
                    user_name = request.session['name']

                    # Retrieve the user based on the name
                    users = get_object_or_404(Uuser, name=user_name)

                    # Check if the cart item already exists for the user and the product
                    cart_item = CartItem.objects.filter(user=users, product_id=product).first()

                    if cart_item:
                        # If the cart item already exists, update its quantity
                        message = 'This item is already in your cart.'
                    else:
                        # If the cart item doesn't exist, create a new one
                        cart_item = CartItem(user=users, product_id=product, quantity=1)
                        message = 'Product added to cart.'

                    # Save the cart item
                    cart_item.save()

                    # Calculate the subtotal for the cart item
                    sub_total = cart_item.sub_total()
                    context = {
                        'cart_items': cart_item,
                        'message': message
                    }

                    # Render the cart template with the cart items and message
                    return render(request, 'wishlist.html', { 'product': product,'message': message})
            else:
                message = 'This product is out of stock.'
            return render(request, 'wishlist.html', { 'product': product,'message': message})


@never_cache
def remove_from_wishlist(request,item_id):
    
    if "password" in request.session:
                 return redirect('admin_home')
    if 'name' in request.session:
        user_name = request.session['name']
        user = get_object_or_404(Uuser, name=user_name)
        item = get_object_or_404(Wishlist, wish_id=item_id, wish_user=user)
        item.delete()
        return redirect('wish')  # Redirect to the cart page after removing the item
    return redirect('login')

@never_cache
def product_detail(request, product_id):
    if "password" in request.session:
                 return redirect('admin_home')
    if "password" in request.session:
        return redirect('admin_home')

    product = get_object_or_404(Product, product_id=product_id)
    products = [product]
    qu = products[0].quantity
    message = ''  # Initialize the message variable with a default value

    if request.method == 'POST':
    
        # Retrieve the product ID from the POST data
        product_id = request.POST.get('product_id')

        # Retrieve the product based on the product ID
        product = get_object_or_404(Product, product_id=product_id)

        if product.quantity > 0:
            if 'name' in request.session:
                # Retrieve the user's name from the session
                user_name = request.session['name']

                # Retrieve the user based on the name
                users = get_object_or_404(Uuser, name=user_name)

                # Check if the cart item already exists for the user and the product
                cart_item = CartItem.objects.filter(user=users, product_id=product).first()

                if cart_item:
                    # If the cart item already exists, update its quantity
                    cart_item.quantity+=1
                    cart_item.save()
                else:
                    # If the cart item doesn't exist, create a new one
                    cart_item = CartItem(user=users, product_id=product, quantity=1)
                    message = 'Product added to cart.'

                # Save the cart item
                cart_item.save()

                # Calculate the subtotal for the cart item
                sub_total = cart_item.sub_total()
                context = {
                    'cart_items': cart_item,
                    'message': message
                }

                # Render the cart template with the cart items and message
                return render(request, 'product.html', {'products': products, 'qu': qu, 'message': message})
        else:
            message = 'This product is out of stock.'

    return render(request, 'product.html', {'products': products, 'qu': qu, 'message': message})




@never_cache
def cart(request):
    if "password" in request.session:
                 return redirect('admin_home')
    a = 120
    print(a)
    if 'name' in request.session:
        user_name = request.session['name']
        user = get_object_or_404(Uuser, name=user_name)
        cart_items = CartItem.objects.filter(user_id=user)
        overall_total = 0
        total = sum(item.product_id.price * item.quantity for item in cart_items)
        print(total)
        if request.method == 'POST':
            print('moooooooooooooooooooooooooooo')
            quantity_exceeded = False
            error_messages = []
            qu = 0
            print(quantity_exceeded)
            
           
            for cart_item in cart_items:
                product_quantity = cart_item.product_id.quantity
                cart_id = request.POST.get('cart_id')
                quantity = int(request.POST.get('quantity'))
                product_id = (request.POST.get('product_id'))
                product = Product.objects.get(product_id=product_id)
                qu = product.quantity
               
                      
                print(qu)
                if cart_item.cart_id == int(cart_id):
                    if qu < quantity:
                        print('helloooooooooooooooooooooooooooooooooooooooo')
                        quantity_exceeded = True
                        error_messages.append({
                            'product_name': cart_item.product_id.name,
                            'error_message': 'Quantity exceeds available stock.'
                        })
                    else:
                        print('haiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
                        cart_item.quantity = quantity
                        cart_item.sub_total = cart_item.product_id.price * quantity
                        cart_item.save()
                        total = sum(item.product_id.price * item.quantity for item in cart_items)
                        print(total)
                        print(cart_item.quantity, cart_item.sub_total, overall_total)
            if quantity_exceeded:
                return render(request, 'cart.html', {'cart_items': cart_items, 'error_messages': error_messages})
            else:
                # return redirect(checkout)
                return render(request, 'cart.html', {'cart_items': cart_items, 'total':total})
        # Replace 'checkout_page' with the appropriate URL name for your checkout page
        return render(request, 'cart.html', {'cart_items': cart_items,"total":total})
    else:
        return redirect('loginn')
from django.http import JsonResponse
# def ajaxQuantity(request):
#     user_name = request.session['name']
#     user = get_object_or_404(Uuser, name=user_name)
#     cart_items = CartItem.objects.filter(user_id=user)
#     item_id=request.GET.get('itemid')
#     print(item_id)
#     quantity=int(request.GET.get('quantity'))
#     cart=CartItem.objects.get(cart_id=item_id)
#     cart.quantity=quantity
#     total_sum = sum(item.quantity * item.product_id.price for item in cart_items)
#     cart.save()
#     total=int(cart.sub_total())
    
#     print(total)
#     return JsonResponse({"total":total,"total_sum":total_sum})   


@never_cache
def ajaxQuantity(request):
    if "password" in request.session:
                 return redirect('admin_home')
    user_name = request.session['name']
    user = get_object_or_404(Uuser, name=user_name)
    cart_items = CartItem.objects.filter(user_id=user)
    item_id = request.GET.get('itemid')
    quantity = int(request.GET.get('quantity'))
    
    cart = CartItem.objects.get(cart_id=item_id)
    original_quantity = cart.product_id.quantity  
    if quantity > original_quantity:
        return JsonResponse({"error": "Exceeded available quantity."})
    
    cart.quantity = quantity
    cart.save()
    
    total_sum = sum(item.quantity * item.product_id.price for item in cart_items)
    total = int(cart.sub_total())
    print(total_sum)
    return JsonResponse({"total": total, "total_sum": total_sum})
# def cart(request):
#     a = 120
#     print(a)
#     if 'name' in request.session:
#         user_name = request.session['name']
#         user = get_object_or_404(Uuser, name=user_name)
#         cart_items = CartItem.objects.filter(user_id=user)
#         if request.method == 'POST':
#             quantity_exceeded = False
#             error_messages = []
#             print(quantity_exceeded)
            
#             for cart_item in cart_items:
#                 product_quantity = cart_item.product_id.quantity
#                 cart_id = request.POST.get('cart_id')
#                 quantity = int(request.POST.get('quantity'))
#                 product_id = request.POST.get('product_id')
                
#                 if cart_item.cart_id == int(cart_id):  # Update only the specific cart item being modified
#                     product = Product.objects.get(product_id=product_id)
#                     if product.quantity < quantity:
#                         quantity_exceeded = True
#                         error_messages.append({'product_name': cart_item.product_id.name,
#                                                'error_message': 'Quantity exceeds available stock.'})
#                     else:
#                         cart_item.quantity = quantity
#                         cart_item.sub_total = cart_item.product_id.price * quantity
#                         cart_item.save()
#                         print(cart_item.quantity, cart_item.sub_total)
                
#             if quantity_exceeded:
#                 return render(request, 'cart.html', {'cart_items': cart_items, 'error_messages': error_messages})
#             else:
#                 # Redirect to the cart page after updating quantities
#                 return redirect('cart')
        
#         return render(request, 'cart.html', {'cart_items': cart_items})
#     else:
#         return redirect('loginn')


@never_cache
def remove_from_cart(request,item_id):
    if "password" in request.session:
                 return redirect('admin_home')
    if 'name' in request.session:
        user_name = request.session['name']
        user = get_object_or_404(Uuser, name=user_name)
        item = get_object_or_404(CartItem, cart_id=item_id, user_id=user)
        item.delete()
        return redirect('add_to_cart')  # Redirect to the cart page after removing the item
    return redirect('login')


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def update_quantity(request):
# 	if request.method == 'POST':
# 		product_id = request.POST.get('product_id')
# 		quantity = request.POST.get('quantity')

# 		# Perform the necessary operations to update the quantity in the database
# 		# Replace the following code with your actual logic
# 		try:
# 			product = Product.objects.get(id=product_id)
# 			product.quantity = quantity
# 			product.save()
# 			success = True
# 		except Product.DoesNotExist:
# 			success = False

# 		# Return a JSON response indicating the success or failure of the update
# 		return JsonResponse({'success': success})
# 	else:
# 		# Handle unsupported request methods
# 		return JsonResponse({'error': 'Invalid request method'})


@never_cache
def checkout(request):
    if "password" in request.session:
                 return redirect('admin_home')
    if 'name' in request.session:
        user_name = request.session['name']
        print('nameeeeeeeeeeeeeeeeee',user_name)
        user = get_object_or_404(Uuser, name=user_name)
        addresses = Address.objects.filter(user_id=user)
        cart_items = CartItem.objects.filter(user_id=user)
        
        for cart_item in cart_items:
            category = str(cart_item.product_id.catogery)
        coup = Coupon.objects.all()
        add=Address.objects.all()
        for i in add:
            print(i)
        total = sum(item.product_id.price * item.quantity for item in cart_items)
        reduction = 0
        subtotal = sum(item.sub_total() for item in cart_items)
        discounted = subtotal
        selected_address = None
        coupon_code = None
        referral_code = None
       
        for add in addresses:
            print(add.address_line)
        if request.method == 'POST':
            address_select = request.POST.get('address_select')
            print(address_select)
            address_line = request.POST.get('address_line')
            state = request.POST.get('state')
            district = request.POST.get('district')
            city = request.POST.get('city')
            referral_code = request.POST.get('referral_code')
            adds=Address(user_id=user, address_line=address_line, state= state,  district=  district,city=city)
            print('adressssssssssss',adds.state)
            adds.save()
            
            if address_select:
                selected_address = Address.objects.get(id=address_select)
                    
            elif addresses:
                selected_address = addresses[0]

            action = request.POST.get('action')


            if action == 'apply_coupon':

                coupon_code = request.POST.get('coupon_code')
                coupon = Coupon.objects.filter(code=coupon_code, active=True).first()
                copuon_category=str(coupon.copuon_category)

                if category==copuon_category:
                    if coupon:
                        discounted = coupon.apply_discount(subtotal)
                        reduction = total - discounted
                        for item in cart_items:
                            item.sub_total=discounted
                            print(item.sub_total)
                            item.save()


            

            for item in cart_items:
                quantity = request.POST.get(f"quantity-{item.product_id}")
                print(quantity,'quantity in the cart') 
                if quantity is not None:
                    quantity = int(quantity)
                    item.quantity = quantity
                    item.save()
                

            if action == 'place_order':
                # Create and save the order
                
                payment_method = request.POST.get('payment_method')

                if payment_method == 'cash_on_delivery':
                     for item in cart_items:
                        product_id=item.product_id
                    # Process cash on delivery order\
                        quantity=item.quantity
                        price=item.product_id.price
                        t_price=quantity*price
                        
                        order = Order(user_id=user, address=selected_address,total_amount=t_price,total_quantity=quantity,product=product_id,payment_method=payment_method)
                        order.save()
                        product_id.quantity -= quantity
                        product_id.save()
                    # Replace the following return statement with the appropriate redirect or response
                     return render(request, 'success.html')

                elif payment_method == 'razorpay':
                    client = razorpay.Client(auth=("rzp_test_LKE4UtUkNNR122", "Ma0iVAjSvXm7CJgE5YdgGenB"))
                    amount = 50000  # Replace with the actual order amount
                    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
                    for item in cart_items:
                        product_id=item.product_id
                        quantity=item.quantity
                        price=item.product_id.price
                        product_id=item.product_id
                    # Process cash on delivery order\
                        quantity=item.quantity
                        price=item.product_id.price
                        t_price=quantity*price
                        order = Order(user_id=user, address=selected_address, total_amount=t_price,total_quantity=quantity,product=product_id,payment_method=payment_method)
                        order.save()
                        product_id.quantity -= quantity
                        product_id.save()
                    # Redirect to the Razorpay payment page
                    return render(request,'rayzor_main.html')
        # for item in cart_items:
        #     quantity = item.quantity
        #     print('haiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiandlklkns')
        #     print(quantity)
        #     item.product_id.quantity -= quantity
        #     item.product_id.save()
        #     print( item.product_id.quantity )
            
                # Redirect to the success page or a relevant page
        print(selected_address)      
        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'addresses': addresses,
            'coup': coup,
            'discounted': discounted,
            'total': total,
            'reduction': reduction,
            'selected_address': selected_address,
            'coupon_code': coupon_code,
            'referral_code': referral_code,
            'coup': coup,
            
        })

    return redirect('loginn')





def Buynow(request):
    if request.method=='POST':
        product=request.POST.get('product_id')

@never_cache
def razor_pay(request):
    if "password" in request.session:
                 return redirect('admin_home')
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 50000
        client = razorpay.Client(
            auth=("rzp_test_LKE4UtUkNNR122", "Ma0iVAjSvXm7CJgE5YdgGenB"))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1','name':name})
    return render(request, 'rayzor_main.html')



@never_cache    
@csrf_exempt
def razor_success(request):
    if "password" in request.session:
                 return redirect('admin_home')
    return render(request, "razor_success.html")



@never_cache

def orders(request):
    if "password" in request.session:
                 return redirect('admin_home')
    if 'name' in request.session:
        user_name = request.session['name']
        user = get_object_or_404(Uuser, name=user_name)
        cart_items = CartItem.objects.filter(user_id=user)
        for i in cart_items:
            print(i.product_id.name,i.sub_total(),i.quantity)
        if request.method == 'POST':
            order_id = request.POST.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            if not order.is_cancelled:
                new_status = request.POST.get('status')
                if new_status in [choice[0] for choice in Order.STATUS]:
                    if new_status == 'Cancelled':
                        order.is_cancelled = True
                    order.status = new_status
                    order.save()
                return redirect('orders')  
        orders = Order.objects.filter(user_id=user)
       
        return render(request, 'order.html', {'user': user, 'orders': orders,'cart_items':cart_items})
    else:
        return redirect('loginn')



@never_cache
def view_orders(request):
   if "password" in request.session:
                 return redirect('admin_home')
   if "password" in request.session:
        
       
            orders = Order.objects.all()
            
            return render(request, 'view_order.html', {'orders': orders})
  
   return redirect('admin_login')



@never_cache
def change_order_status(request, order_id):
    
    if "password" in request.session and request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in Order.STATUS]:
            if new_status == 'Cancelled':
                order.cancel_order()
            else:
                order.status = new_status
                order.save()
                if order.status=="Returned":
                     order.product.quantity+=order.total_quantity
                     order.product.save()

        return redirect('view_orders')
    else:
        return redirect('admin_login')
 
@never_cache   

def cancel_order(request):
    print('haii11111111111111111146757')
    if "password" in request.session:
                 return redirect('admin_home')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        if not order.is_cancelled:
            order.is_cancelled = True
            order.status = 'Cancelled'
           
            
            order.save()
            order.product.quantity+=order.total_quantity
            order.product.save()
            print(order.product.quantity)
            return redirect('orders')


@never_cache
def coupon_view(request):
    if "password" in request.session:
        search = request.GET.get('search')
        if search:
            coup = Coupon.objects.filter(name__istartswith=search)
        else:
            coup = Coupon.objects.all()
        
        return render(request, 'coupon_view.html', {'coup': coup})
    else:
        return redirect('admin_login')


def add_coupon(request):
   if "password" in request.session:
    if request.method == 'POST':
        code = request.POST.get('code')
        discount = request.POST.get('discount')
        referral_code = request.POST.get('referral_code')
        valid_from= request.POST.get(' valid_from')
        valid_to = request.POST.get(' valid_to')
        
        coup = Coupon.objects.create(
            code =code,
            discount=discount,
            referral_codee=referral_code,
            valid_from=valid_from,
            valid_to=valid_to

        )

        return redirect(coupon_view)

    return render(request, 'add_coupon.html')
   else:
    return redirect('admin_login')
   


@never_cache
def delivered_products(request):
    if "password" in request.session:
                 return redirect('admin_home')
    mes = ''
    # Retrieve delivered products from the database
    delivered_product = Order.objects.filter(status='Delivered')
    if request.method == 'POST':
        
        order_id=request.POST.get('order_id')
         # Set an initial empty value for mes
        order=Order.objects.get(id=order_id)
        order.is_returned=True
        order.return_status = 'Pending'
        order.save()
        print(order.is_returned)
        
        return redirect('deli')
        # return render(request, 'deliverd_pro.html', {'order': order, 'mes': mes})
    return render(request, 'deliverd_pro.html', {'delivered_product': delivered_product,'mes':mes})
from django.contrib import messages



@never_cache
def view_delivered_products(request):
    if 'password' in request.session:
       
       delivered_product = Order.objects.filter(status='Delivered')

       return render(request, 'view_deliverd_pro.html', {'delivered_product': delivered_product})
 
@never_cache   
def view_returned_products(request):
    if 'password' in request.session:
       ret = Order.objects.filter(status='Returned')
       return render(request, 'view_returned.html', {'ret':ret})

@never_cache    
def returned_products(request):
    if "password" in request.session:
                 return redirect('admin_home')
    if 'name' in request.session:
       retn = Order.objects.filter(status='Returned')
       return render(request, 'returned_pro.html', {'retn':retn})




# def return_product(request):
#      if request.method == 'POST':
#         order_id=request.POST.get('order_id')
#         mes = ''  # Set an initial empty value for mes
#         order=Order.objects.get(id=order_id)
#             # Update the return status of the order
#         order.return_status = 'Pending'
#         order.save()
#         if order.return_status == "Pending":
#             mes = 'success pending'
        
#         return render(request, 'deliverd_pro.html', {'order': order, 'mes': mes})


@never_cache  

def confirm_return(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        # Update the return status of the order
        order.return_status = 'Confirmed'
        order.save()
       
        # Display a success message
        messages.success(request, 'Return confirmed.')
        # Redirect to a relevant page
        return redirect('admin_return_confirmation')
    return render(request, 'admin_confirm_return.html', {'order': order})