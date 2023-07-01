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
from django.core.paginator import Paginator
import matplotlib.pyplot as plt
plt.switch_backend('Agg') 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import csv
from django.http import FileResponse
import io
import vonage
from django.db.models import Sum
import calendar
from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Sum
from datetime import *
client = vonage.Client(key="49f664eb", secret="fFe4DCMVuzhsv1pr")
sms = vonage.Sms(client)
# Create your views here.
@never_cache
def registerform(request):
    user=None
    if "password" in request.session:
        return redirect("admin_home.html")
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
        error = {}
        us=Uuser.objects.all()
        n=[i.phone_number for i in us]
        l=[em.email for em in us]
        for ll in n:
            print("pp",ll)
        s=[i.name for i in us]
        if not name:
            error["name"] = 'Name is required'
        if name in s:
            error["name"]='same name exist please enter another'
        if len(name) < 4:
             error["name"] = 'Name must be longer than 4 characters'
        
        if not re.match(r'^[\w-]+(\.[\w-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,})$', email):
            error['email'] = 'Enter a valid email address'
        if email in l:
            error['email'] = 'Email already exists'
        if not re.match(r"^\d{10}$",phone_number):
                  error ['phone_number']= 'enter numbers'
        if len(phone_number) < 10:
            error ['phone_number']= 'Phone number should contain 10 characters or numbers'
       
        if len(password) < 4:
            error["password"] = 'Password should contain at least 4 characters or numbers'
        if password!=repassword:
            error["repassword"]="not match"
        if error is None:
            print("haii")
        if  not error:
            user = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phoneNumber': request.POST.get('phone_number'),
            'password': request.POST.get('password'),
        }
            request.session['user']=user
            try:
                otp = str(random.randint(0, 9999)).zfill(4)
                print(otp)
                request.session['otp'] = otp
                send_sms(otp, request.POST['phone_number'])
            except Exception as e:
                print(e)
            return redirect(otp_grn,otp)   
        else:
         return render(request,'signup.html',{'error':error,"user":user}) 
    else:
        print("haiii00")
        return render(request, 'signup.html',{"user":user})
    

def send_sms(otp, phone_number):
    try:
        body = {
            "authorization": "9mCRNewf4y51lc6KJLFYIgZtEjxv0WV3PuoHOra2BphzsGUMiqwmdFs3TZfEMB2vkcG5JqNeRSyCj8Yp",
            "variables_values": otp,
            "route": "otp",
            "numbers": phone_number,
        }
        
        response = requests.get("https://www.fast2sms.com/dev/bulkV2", json=body)
        return response
    except Exception as e:
        print(e)


@never_cache
def otp_grn(request, otp):
    if request.method == 'POST':
        if request.POST.get('otp') == otp:
            user_data = request.session.get('user')

            if user_data:
                name = user_data.get('name')
                email = user_data.get('email')
                phone_number = user_data.get('phoneNumber')
                password = user_data.get('password')
                repassword = user_data.get('password')
                form = Uuser(name=name, email=email, password=password, repassword=repassword,
                             phone_number=phone_number)
                form.save()
                del request.session['user']
                # OTP is valid, redirect to the home page
                return redirect('loginn')
        else:
            # OTP is invalid, render the OTP verification page again with an error message
            msg = 'Enter valid OTP'
            return render(request, 'otp.html', {'msg': msg})
    else:
        # Render the OTP verification page
        return render(request, 'otp.html')
    



def guest_registerform(request):
    if "password" in request.session:
        return redirect("admin_home.html")
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
        error = {}
        us=Uuser.objects.all()
        n=[i.phone_number for i in us]
        l=[em.email for em in us]
        for ll in n:
            print("pp",ll)
        s=[i.name for i in us]
        if not name:
            error["name"] = 'Name is required'
        if name in s:
            error["name"]='same name exist please enter another'
        if len(name) < 4:
             error["name"] = 'Name must be longer than 4 characters'
    
        if not re.match(r'^[\w-]+(\.[\w-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,})$', email):
            error['email'] = 'Enter a valid email address'
        if email in l:
            error['email'] = 'Email already exists'
        if int(phone_number) in n:
                error ['phone_number']="number already exists"
        if len(phone_number) < 10:
            error ['phone_number']= 'Phone number should contain 10 characters or numbers'
       
        if len(password) < 4:
            error["password"] = 'Password should contain at least 4 characters or numbers'
        if password!=repassword:
            error["repassword"]="not match"
        if error is None:
            print("haii")
        if  not error:
            user = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phoneNumber': request.POST.get('phone_number'),
            'password': request.POST.get('password'),
        }
            request.session['user']=user
            try:
                otp = str(random.randint(0, 9999)).zfill(4)
                print(otp)
                request.session['otp'] = otp
                guest_send_sms(otp, request.POST['phone_number'])
            except Exception as e:
                print(e)
            return redirect(otp_grn,otp)   
        else:
         return render(request,'signup.html',{'error':error}) 
    else:
        print("haiii00")
        return render(request, 'signup.html')
    

def guest_send_sms(otp, phone_number):
    try:
        body = {
            "authorization": "9mCRNewf4y51lc6KJLFYIgZtEjxv0WV3PuoHOra2BphzsGUMiqwmdFs3TZfEMB2vkcG5JqNeRSyCj8Yp",
            "variables_values": otp,
            "route": "otp",
            "numbers": phone_number,
        }
        
        response = requests.get("https://www.fast2sms.com/dev/bulkV2", json=body)
        return response
    except Exception as e:
        print(e)


@never_cache
def guest_otp_grn(request, otp):
    if request.method == 'POST':
        if request.POST.get('otp') == otp:
            user_data = request.session.get('user')

            if user_data:
                name = user_data.get('name')
                email = user_data.get('email')
                phone_number = user_data.get('phoneNumber')
                password = user_data.get('password')
                repassword = user_data.get('password')
                form = Uuser(name=name, email=email, password=password, repassword=repassword,
                             phone_number=phone_number)
                form.save()
                
                # OTP is valid, redirect to the home page
                return redirect('loginn')
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
            user=Uuser.objects.filter(name=name).first()
            cart_items = CartItem.objects.filter(user_id=user)

            if not cart_items:
                guest=Guest.objects.all()
                for i in guest:
                    cart=CartItem(cart_id=i.guest_id,user=user,variant_id=i.guest_variant_id,quantity=i.guest_quantity)
                    cart.save()
                guest.delete()
            
            
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
              return redirect(admin_home)
          else:
              dict= 'invalid Name or password..!'
  return render(request, 'admin_login.html',{'dict':dict})

@never_cache
def admin_home(request):
    if "password" in request.session:
                ors=Order.objects.all()
                c=0
                m=0
                l=0
                j=0
                for i in ors:
                    c+=i.total_quantity
                    c=int(c)
                    m+=i.total_amount
                    m=int(m)
                for i in ors:
                    if i.status=="Cancelled" or i.status=="Returned":
                        l+=i.total_quantity
                        j+=i.total_amount
                        l=int(l)
                        j=int(j)
                dq={}
                d=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                for i in ors:
                    print(i.order_date.strftime('%A'),i.total_quantity)
                    if i.status !="Cancelled" and i.status !="Returned":
                        if i.order_date.strftime('%A') not in dq:
                            dq[i.order_date.strftime('%A')]=i.total_quantity
                        else:
                            dq[i.order_date.strftime('%A')]+=i.total_quantity 
                for i,j in dq.items():

                        print('haii',i,j)
                mq={}
                for i in ors:
                    print(i.order_date.strftime('%B'),i.total_quantity)
                    if i.status !="Cancelled" and i.status !="Returned":
                        if i.order_date.strftime('%B') not in mq:
                            mq[i.order_date.strftime('%B')]=i.total_quantity
                        else:
                            mq[i.order_date.strftime('%B')]+=i.total_quantity 

                yq={}
                for i in ors:
                    print(i.order_date.strftime('%Y'),i.total_quantity)
                    if i.status !="Cancelled" and i.status !="Returned":
                        if i.order_date.strftime('%Y') not in yq:
                            yq[i.order_date.strftime('%Y')]=i.total_quantity
                        else:
                            yq[i.order_date.strftime('%Y')]+=i.total_quantity 
                return render(request, "admin_home.html",{"yq":yq,"mq":mq,"dq":dq,"c":c,"m":m,"l":l,"j":j}) 
    else:
       return render(request,"admin_login.html",)

def invoice(request):
    return render(request,"invoice.html")


def user_venue_pdf(request):
    if request.method == 'POST':
        order_id=request.POST.get("order_id")
        venues=Order.objects.filter(id=order_id)
        print(venues)
        # buf = io.BytesIO()
        # 
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)


        data = []
        data.append(['Name', 'Product', 'Address', 'Payment Type',"amount","quantity", 'Order Status', 'Order Date'])
        for venue in venues:
            data.append([str(venue.id),
            venue.varient_Key.product_key.name,
            (str(venue.address.address_line)),
            (str(venue.payment_method)),
            (str(venue.total_amount)),
             (str(venue.total_quantity)),
            (str(venue.status)),
            (str(venue.order_date))
            ])
            table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements = []
        elements.append(table)
        doc.build(elements)
        buf.seek(0)

        return FileResponse(buf,as_attachment=True, filename='venue.pdf')
    return render(request,'order.html')
def venue_pdf(request):
    if request.method=='POST':
        startdate= request.POST.get('startdate')
        enddate= request.POST.get('enddate')
        download_all = request.POST.get('download_all')
        print(download_all)
        if download_all:
            venues = Order.objects.all()
        
        elif enddate =='' or startdate =='':
            error_date='Both fields to be filled'
            return render(request,'invoice.html',{'startdate':startdate,'error_date':error_date})
        elif startdate == enddate:
            error_date='The start date and end date cannot be equal. Please choose the right date range.'
            return render(request,'invoice.html',{'startdate':startdate,'enddate':enddate,'error_date':error_date})
        elif startdate > enddate:
            error_date='The start date cannot be greater than the end date .Please choose the right date'
            return render(request,'invoice.html',{'error_date':error_date})

            
        else:
            venues=Order.objects.filter(order_date__range=(startdate,enddate))
            print(venues)
        # buf = io.BytesIO()
        # 
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)


        data = []
        data.append(['Name', 'Product', 'Address', 'Payment Type', 'Order Status', 'Order Date'])
        for venue in venues:
            data.append([str(venue.id),
            venue.varient_Key.product_key.name,
            (str(venue.address.address_line)),
            (str(venue.payment_method)),
            (str(venue.status)),
            (str(venue.order_date))
            ])
            table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 14),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))

        elements = []
        elements.append(table)
        doc.build(elements)
        buf.seek(0)

        return FileResponse(buf,as_attachment=True, filename='venue.pdf')
    return render(request,'invoice.html')

def excel(request):
    if request.method == 'POST':
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        download_all = request.POST.get('download_all')
        if download_all:
            venues = Order.objects.all()
        elif enddate == '' or startdate == '':
            error_date='Both fields to be filled'
            return render(request,'excel.html',{'startdate':startdate,'error_date':error_date})

        elif startdate == enddate:
            error_date='The start date and end date cannot be equal. Please choose the right date range.'
            return render(request,'excel.html',{'startdate':startdate,'enddate':enddate,'error_date':error_date})
        elif startdate > enddate:
            error_date = 'The start date cannot be greater than the end date. Please choose the right date.'
            return render(request, 'excel.html', {'error_date': error_date})
        else:
            venues = Order.objects.filter(order_date__range=(startdate, enddate))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="venue.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Product', 'Address', 'Payment Type', 'Order Status', 'Order Date'])

        for venue in venues:
            writer.writerow([str(venue.id), venue.varient_Key.product_key.name, str(venue.address.address_line), str(venue.payment_method), str(venue.status), str(venue.order_date)])
        return response
    return render(request, 'excel.html')



@never_cache
def admin_logout(request):
  if "password" in request.session:
    del request.session['password']
    return redirect('admin_login')
  else:
      return redirect('admin_login')
  

@never_cache 
def user_list(request):
    if "password" in request.session:
        search = request.GET.get('search')
        if search:
            users = Uuser.objects.filter(name__istartswith=search)
            paginator=Paginator(users,5)
            page_number=request.GET.get("page")
            page_obj = paginator.get_page(page_number)
        else:
            users = Uuser.objects.all()
            paginator=Paginator(users,1)
            page_number=request.GET.get("page")
            page_obj = paginator.get_page(page_number)
        
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
        
        return render(request, 'userlist.html', {'users':users,'page_obj':page_obj})
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
            paginator=Paginator(cato,5)
            page_number=request.GET.get("page")
            page_obj = paginator.get_page(page_number)
        else:
            cato = category.objects.all()
            paginator=Paginator(cato,5)
            page_number=request.GET.get("page")
            page_obj = paginator.get_page(page_number)
        return render(request, 'view_catogery.html', {'cato': cato,"page_obj":page_obj})
    else:
        return redirect('admin_login')



@never_cache
def add_catogery(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        descrition= request.POST.get('descrition')
        catewise_dicount_price=request.POST.get('catewise_dicount_price')
        # Retrieve the category object based on the submitted name
        c=category.objects.all()
        s=[i.name for i  in c]
        error=None
        if name:
            if len(name)<4 or len(name)>15:
                error='Name must longer than 4' 
            if name in s:
                error=' same name exist,please give another name'
        if error:
            return render(request, 'add_catogery.html',{'error':error})
       

        cato = category.objects.create(
            name=name,
           descrition=descrition,
           catewise_dicount_price=catewise_dicount_price
        )
        cato.save()
        return redirect(view_category)

    return render(request, 'add_catogery.html')


@never_cache

def edit_category(request,id):
    cato = get_object_or_404(category, id=id)

    if request.method == 'POST':
        cato.name = request.POST.get('name')
        cato.descrition= request.POST.get('descrition')
        cato.catewise_dicount_price= request.POST.get('catewise_dicount_price')

        cato.save()
        return redirect('viewcatogery')
    else:
        context = {'cato': cato}
        return render(request, 'edit_catogery.html', context)
    
def edit_coupon(request,id):
    cato = get_object_or_404(Coupon, id=id)

    if request.method == 'POST':
        cato.code = request.POST.get('code')
        cato.coupon_dis_amount= request.POST.get('coupon_dis_amount')
        cato.coupon_minmun_amount= request.POST.get('coupon_minmun_amount')
        cato.valid_from= request.POST.get('valid_from')
        cato.valid_to= request.POST.get('valid_to')

        cato.save()
        return redirect(coupon_view)
    else:
        context = {'cato': cato}
        return render(request, 'edit_coup.html', context)
    
def delete_coup(request,id):
    cato=Coupon.objects.get(id=id)
    cato.delete()

@never_cache
def delete_category(request,id):
   cato=category.objects.get(id=id)
   cato.delete()
   return redirect(view_category) 
def delete_variant(request,id):
   cato=Varient.objects.get(id=id)
   cato.delete()
   return redirect(view_variant) 


def delete_address(request,id):
   cato=Address.objects.get(id=id)
   cato.delete()
   return redirect("pro") 

@never_cache
def product_view(request):
    if "password" in request.session:
        search = request.GET.get('search')
        if search:
            products = Product.objects.filter(name__istartswith=search)
            paginator = Paginator(products, 2)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            products = Product.objects.all()
            paginator = Paginator(products, 2)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        return render(request, 'product_view.html', {'products': products,'page_obj':page_obj})
    else:
        return redirect('admin_login')

@never_cache
def add_product(request):
   if "password" in request.session:
    categories = category.objects.all()
    if request.method == 'POST':
        p_name = request.POST.get('name')
        catogery_name = request.POST.get('catogery')
        description = request.POST.get('description')
        print(catogery_name)
        catogery = category.objects.get(name=catogery_name)
        p=Product.objects.all()
       
       
        n=[product.name for product in p]
        
        error=None
        
       
        if len(p_name)<4:
            error='Name must longer than 4' 
        if p_name in n:
            error=' same name exist,please give another name'
        if len(catogery_name)<1:
            error='Name must longer than 1' 
        if error:
            return render(request, 'add.html',{'error':error,"categories":categories})
        
        
        else:
        # Create the Product object with the correct category ID
            product = Product.objects.create(
                name=p_name,
                catogery=catogery,
                description=description,
            )

            product.save()
            return redirect(product_view)
    return render(request, 'add.html',{"categories":categories})
   else:
    return redirect('admin_login')
def view_variant(request):
    if "password" in request.session:
        search = request.GET.get('search')

        if search:
            vari = Varient.objects.filter(varient_name__istartswith=search)
            paginator = Paginator(vari, 2)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
         vari = Varient.objects.all()
         paginator = Paginator(vari, 2)
         page_number = request.GET.get('page')
         page_obj = paginator.get_page(page_number)
        return render(request, 'view_variant.html', {'vari': vari,"page_obj":page_obj})
    else:
        return redirect('admin_login')


def add_variant(request):
   if "password" in request.session:
    product=Product.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        varient_name=request.POST.get('variant')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        off=request.POST.get('offer price')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        error=None
        k=[]
        l = Varient.objects.filter(varient_name=varient_name)
        if l.exists():
            variant = l.first()  # Retrieve the first variant from the queryset
            pro = variant.product_key
            k.append(pro)
       
        
        if  varient_name:
            if len( varient_name)<2:
                error='Name must longer than 4' 
            if  varient_name in k:
                error=' same name exist,please give another name'
         
        if quantity:
           if int(quantity)<=0:
             error= " quantity must be greater than 0"
        if price:
            if int(price)<=0:
               error= " price must be greater than 0" 
            
                  
        if error:
            return render(request, 'add_variant.html',{'error':error,"product":product})
        # Create the Product object with the correct category ID
        product = Product.objects.get(
            name=name,
            
        )
        variant= Varient.objects.create(
            product_key=product,
            varient_name=varient_name,
            quantity=quantity,
            price=price,
            catogery_offer_price=off,
            image=image1,
            image1=image2,
            image2=image3
        )
        variant.save()
        return redirect(product_view)
    return render(request, 'add_variant.html',{"product":product})
   else:
    return redirect('admin_login')
       


@never_cache
def edit_variant(request, product_id):
    prod = get_object_or_404(Varient, id=product_id)
    pro=Product.objects.all()
    if request.method == 'POST':
        prod.varient_name = request.POST.get('name')
        prod.price = request.POST.get('price')
        prod.catogery_offer_price= request.POST.get('offer price')
        prod.quantity = request.POST.get('quantity')

        # Check if new images are provided
        if 'image' in request.FILES:
        # Delete the existing image1 file
            if prod.image:
                os.remove(prod.image.path)
            prod.image = request.FILES.get('image')
      
        if 'image1' in request.FILES:
            # Delete the existing image2 file
            if prod.image1:
                os.remove(prod.image1.path)
            prod.image1 = request.FILES.get('image1')
       
        if 'image2' in request.FILES:
            # Delete the existing image3 file
            if prod.image2:
                os.remove(prod.image2.path)
            prod.image2 = request.FILES.get('image2')
       

        product_name = request.POST.get('product')
        cat_obj, _ = Product.objects.get_or_create(name=product_name)
        prod.product_key = cat_obj
        # Retrieve the category if it exists, otherwise create a new category
        
        
        prod.save()
        return redirect('viewvariant')
    else:
        context = {'prod': prod,"pro":pro}
        return render(request, 'edit.html', context)



@never_cache
def delete_product(request, product_id):
   product=Product.objects.get(product_id=product_id)
   product.delete()
   return redirect(product_view) 


# def home_2(request):
#     return render(request,'home-03.html')


def shop(request):
    user=None
    if "password" in request.session:
        return redirect('admin_home')
    else:
            user = request.session.get('name')
            search = request.GET.get('search')
            categry_filter = request.GET.get('name')
            
            price_range_filter = request.GET.get('price_range')
            l=[]
            print(price_range_filter)
            of=None
            # Filter products based on search query
            if search:

                products = Product.objects.filter(name__istartswith=search)
            else:
                product = Product.objects.all()
                print(product)
                
                for item in product:
                    variant = Varient.objects.filter(product_key=item.product_id).first()
                    print(variant.id)
                    l.append((variant))
                    print(l)
            # Apply category filte
            if categry_filter:
                l = []
                category_instance = category.objects.get(name=categry_filter)
                products = Product.objects.filter(catogery_id=category_instance)
                for product in products:
                    variant = Varient.objects.filter(product_key=product).first()

                    l.append(variant)


           
            if price_range_filter:
                min_price, max_price = map(int, price_range_filter.split('-'))
                products = Product.objects.all()
                l = []
                for product in products:
                    variant = Varient.objects.filter(product_key=product).first()
                    if variant and min_price <= variant.price <= max_price:
                        
                        l.append((variant))


           
            if request.method == 'POST':
            # Retrieve the product ID from the POST data
                product_id = request.POST.get('product_id')

                # Retrieve the product based on the product ID
                
                product = get_object_or_404(Varient, id=product_id)
                
                if 'name' in request.session:
                    # Retrieve the user's name from the session
                    user_name = request.session['name']

                    # Retrieve the user based on the name
                    users = get_object_or_404(Uuser, name=user_name)

                    # Check if the cart item already exists for the user and the product
                    wish_item = Wishlist.objects.filter(wish_user=users, wish_product=product).first()

                    if wish_item:                  # If the cart item already exists, update its quantity
                     messages.info(request, 'This item is already in your list.')
                    
                    else:
                        # If the cart item doesn't exist, create a new one
                        wish_item =Wishlist(wish_user=users, wish_product=product)

                    # Save the cart item
                    wish_item.save()
            if 'name' in request.session:
                user_name = request.session['name']
                user = get_object_or_404(Uuser, name=user_name)
                return render(request, 'shop.html', {'l': l,"product":product,'of':of,"user":user})
            return render(request, 'shop.html', {'l': l,"product":product,'of':of,"user":user})
    
   
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
            product = Varient.objects.get(id=product_id)
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
            product = get_object_or_404(Varient,id=produ)

            if product.quantity > 0:
                if 'name' in request.session:
                    # Retrieve the user's name from the session
                    user_name = request.session['name']

                    # Retrieve the user based on the name
                    users = get_object_or_404(Uuser, name=user_name)

                    # Check if the cart item already exists for the user and the product
                    cart_item = CartItem.objects.filter(user=users, variant_id=product)

                    if cart_item:
                        # If the cart item already exists, update its quantity
                        message = 'This item is already in your cart.'
                    else:
                        # If the cart item doesn't exist, create a new one
                        cart_item = CartItem(user=users, variant_id=product, quantity=1)
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
import json
@never_cache

def product_detail(request, product_id):
    user=None
    if "password" in request.session:
        return redirect('admin_home')
    varient=Varient.objects.get(id=product_id)

    p_id=varient.product_key
    
    all_variants= Varient.objects.filter(product_key=p_id)
    product = Varient.objects.all()
    
    
    prducts = [product]
    producs=prducts[0]
    products=producs[0]
    
    qu = producs[0].quantity
    print(qu)
    message = ''  # Initialize the message variable with a default value
    if 'name' in request.session:
        if request.method == 'POST':
        
            # Retrieve the product ID from the POST data
            varient_id = request.POST.get('varient_id')

            # Retrieve the product based on the product ID
            prod = get_object_or_404(Varient, id= varient_id )

            if prod.quantity > 0:
                if 'name' in request.session:
                    # Retrieve the user's name from the session
                    user_name = request.session['name']

                    # Retrieve the user based on the name
                    users = get_object_or_404(Uuser, name=user_name)

                    # Check if the cart item already exists for the user and the product
                    cart_item = CartItem.objects.filter(user=users, variant_id=prod).first()

                    if cart_item:
                        # If the cart item already exists, update its quantity
                        cart_item.quantity+=1
                        cart_item.save()
                    else:
                        # If the cart item doesn't exist, create a new one
                        cart_item = CartItem(user=users, variant_id=prod, quantity=1)
                        message = 'Product added to cart.'

                        # Save the cart item
                        cart_item.save()

                    # Calculate the subtotal for the cart item
                    # sub_total = cart_item.sub_total()
                    # context = {
                    #     'cart_items': cart_item,
                    #     'message': message
                    # }

                    # Render the cart template with the cart items and message
                    return render(request, 'product.html', {"user":user,"all_variants":all_variants,'varient':varient,'products': products,'product': product, 'qu': qu, 'message': message})
    else:
                if request.method == 'POST':
        # Retrieve the product ID from the POST data
                    varient_id = request.POST.get('varient_id')
                    # Retrieve the product based on the product ID
                    prod = get_object_or_404(Varient, id= varient_id )
                cart_item = Guest.objects.filter(guest_variant_id=varient).first()
                print("hai cart", cart_item)
                if cart_item:
                    cart_item.guest_quantity+= 1
                    cart_item.save()
                    print('im session')
                else:
                    print('im not the session')
                    # cart_item = Guest(guest_variant_id=varient, guest_quantity=0)
                    # cart_item.save()
                    cart=Guest.objects.create(guest_variant_id=varient,guest_quantity=0)
                    # cart_item_data = {
                    #             'variant_id': cart_item.variant_id.id,
                    #             'quantity': cart_item.quantity,
                    #             'image':cart_item.variant_id.image.url,
                    #             'name':cart_item.variant_id.product_key.name,
                    #             'price':int(cart_item.variant_id.price)
                    #             # Add more attributes as needed
                    #         }
                    #                     # Convert the CartItem object to a dictionary
                    
                    # request.session["cart_item_data"]=cart_item_data
                    
                    
    # else:         print
    #     message = 'This product is out of stock.'
    
    return render(request, 'product.html', {"user":user,"all_variants":all_variants,'varient':varient,'products': products,'product': product, 'qu': qu, 'message': message})



def forgot_password(request):
    if request.method=='POST':
        name=request.POST.get("name")
        phone=request.POST.get("phone")
        user = get_object_or_404(Uuser, name=name)
        print(name)
        if  user:
            request.session["user"]=user.name
            try:
                        otp = str(random.randint(0, 9999)).zfill(4)
                        print(otp)
                        request.session['otp'] = otp
                        send_sms(otp, phone)
            except Exception as e:
                        print(e)
            return redirect(forget_otp_grn,otp)
        else:
            error="not correct name"       
            return render(request,"phone.html",{"error":error})
    return render(request,"phone.html")


def forget_otp_grn(request,otp):
    if request.method == 'POST':
        otp=request.session.get("otp")
        if request.POST.get('otp') == otp:
                # OTP is valid, redirect to the home page
                return redirect('editpass')
        else:
            # OTP is invalid, render the OTP verification page again with an error message
            msg = 'Enter valid OTP'
            return render(request, 'otp.html', {'msg': msg})
    else:
        # Render the OTP verification page
        return render(request, 'otp.html')


def edit_password(request):
    user_name = request.session['user']
    user = get_object_or_404(Uuser, name=user_name)
    
    if request.method=="POST":
        new = request.POST.get('new_password')
        re_new= request.POST.get('re_new_password')
        print(new,re_new)
        if new==re_new:
                user.password=re_new
                user.save() 
                return redirect("loginn")
        else:
                    error="not match"
                    return render(request,"edit_pass.html,",{"error":error})
    else:
           return render(request,"edit_pass.html")
    

def variantselection(request):
    products = Varient.objects.all()
    product = products[0]  # Assuming you only need the first product
    all_variants = None
    variant = None
    message = ''
    qu = product.quantity
    if 'name' in request.session:
        if request.method == "POST":
            action = request.POST.get('action')
            if action == "selection":
                v_id = request.POST.get("variant_id")
                varient = Varient.objects.get(id=v_id)
                print('this is selected........',varient.id)
                p_id = varient.product_key
                all_variants = Varient.objects.filter(product_key=p_id)
                message = 'Variant selected.'
            if action == "add_to_cart":
                v_id = request.POST.get("varient_id")
                print('no iddddddddddddddddddddddd')
                print(v_id)
                varient = Varient.objects.get(id=v_id)
                p_id = varient.product_key
                all_variants = Varient.objects.filter(product_key=p_id)
                print(varient.varient_name)
                if varient.quantity > 0:
                    if 'name' in request.session:
                        user_name = request.session['name']
                        users = get_object_or_404(Uuser, name=user_name)
                        cart_item = CartItem.objects.filter(user=users, variant_id=varient).first()
                        if cart_item:
                            cart_item.quantity += 1
                            cart_item.save()
                        else:
                            cart_item = CartItem(user=users, variant_id=varient, quantity=1)
                            message = 'Product added to cart.'
                            cart_item.save()

                        sub_total = cart_item.sub_total()
                        context = {
                            'cart_items': cart_item,
                            'message': message
                        }
                        return render(request, 'product.html', {"all_variants":all_variants,'varient':varient,'products': products,'product': product, 'qu': qu, 'message': message})
    else:
            print("im guest")
            if request.method == "POST":
                action = request.POST.get('action')

                if action == "selection":
                    v_id = request.POST.get("variant_id")
                    varient = Varient.objects.get(id=v_id)
                    print('this is selected........',varient.id)
                    p_id = varient.product_key
                    all_variants = Varient.objects.filter(product_key=p_id)
                    message = 'Variant selected.'
                if action == "add_to_cart":
                    v_id = request.POST.get("varient_id")
                    print('no iddddddddddddddddddddddd')
                    print(v_id)
                    varient = Varient.objects.get(id=v_id)
                    p_id = varient.product_key
                    all_variants = Varient.objects.filter(product_key=p_id)
                    print(varient.varient_name)
    # Retrieve the product ID from the POST data
                # Retrieve the product based on the product ID
                    prod = get_object_or_404(Varient, id= v_id )
                    cart_item = Guest.objects.filter(guest_variant_id=varient).first()
                    print("hai cart", cart_item)
                    if cart_item:
                        cart_item.guest_quantity += 1
                        cart_item.save()
                        print('im session')
                    else:
                        print('im not the session')
                        cart_item = Guest(guest_variant_id=varient, guest_quantity=1)
                        cart_item.save()
    return render(request, 'product.html', {"all_variants": all_variants, 'varient': varient, 'products': products, 'product': product, 'qu': qu, 'message': message})

        
def get_variant_details(request):
    variant_id = request.GET.get('variant_id')
    try:
        variant = Varient.objects.get(id=variant_id)
        print(variant.name)
        # Construct the response data
        data = {
            'varient_name': variant.varient_name,
            'quantity': variant.quantity,
            'price': str(variant.price),
            # Add other fields as needed
        }
        return JsonResponse(data)
    except Varient.DoesNotExist:
        return JsonResponse({'error': 'Variant not found'}, status=404)


def check(request):
 if 'name' in request.session:
    name=request.session['name']
    print(name)
    c=Couponapplied.objects.all()
    for i in c:
      print(i.c_user,i.c_code)
    user  = Uuser.objects.get(name=name)
    addresses=Address.objects.filter(user_id=user)
    li=[]
    for i in addresses:
        li.append(i)
    print(li)
    cart_items = CartItem.objects.filter(user_id=user)
    first_coupon = Coupon.objects.first()
  
    total=0
    # total = sum(item.variant_id.price * item.quantity for item in cart_items)
    for i in cart_items:
        if i.variant_id.catogery_offer_price==0:
            total+=i.variant_id.price * i.quantity
        else :
            total+=i.variant_id.catogery_offer_price * i.quantity
    reduction = 0
    selected_address=None
    subtotal = sum(item.sub_total() for item in cart_items)
    discounted = subtotal
    coup=Coupon.objects.all()
    coupon_code = coup.first()
    n = []
    s = []
    catogery_offer_available = None

    for item in cart_items:
        n.append(item.variant_id.product_key.catogery.catewise_dicount_price)
        s.append(item.variant_id.product_key.catogery.name)

    for i in range(len(n)):
        if n[i] > 0:
            catogery_offer_available = s[i]
        print(catogery_offer_available)
    if request.method == 'POST':
        action = request.POST.get('action')
        address_select = request.POST.get('address_select')
        address_line = request.POST.get('address_line')
        state = request.POST.get('state')
        district = request.POST.get('district')
        city = request.POST.get('city')
        
        if address_select:
            print(address_select)
            selected_address = Address.objects.get(id=address_select)
        if address_line and state and district and city:
            new_address = Address(user_id=user, address_line=address_line, state=state, district=district, city=city)
            new_address.save()
            selected_address = new_address
            print(new_address)
        addresses = Address.objects.filter(user_id=user)
        for item in cart_items:
                product_id=item.variant_id.product_key
            # Process cash on delivery order\
                quantity=item.quantity
                price=item.variant_id.price
                t_price=quantity*price
       
        error=None
        if action == 'place_order':
                # Create and save the order
                
                        payment_method = request.POST.get('payment_method')
                        print("method",payment_method)
                    
                        if payment_method == 'cash_on_delivery':
                         if cart_items:
                            if address_select:
                                for item in cart_items:
                                    product_id=item.variant_id
                                    quantity=item.quantity
                                    price=item.variant_id.price
                                    t_price=quantity*price
                                    
                                    if item.variant_id.catogery_offer_price==0:
                                        t_total=item.variant_id.price * quantity
                                        print(total)
                                    else :
                                        t_total=item.variant_id.catogery_offer_price * quantity
                                        print(total)
                                    print(total)
                                    order = Order(user_id=user, address=selected_address,total_amount=t_total,total_quantity=quantity,varient_Key=product_id,payment_method=payment_method)
                                    order.save()
                                    product_id.quantity -= quantity
                                    product_id.save()
                                if "coupon" in request.session:
                                  coupon=request.session.get("coupon")
                                  applied=Couponapplied.objects.create(c_code=coupon,c_user=user)
                               
                                  del request.session["coupon"]
                               
                                cart_items.delete()
                            # Replace the following return statement with the appropriate redirect or response
                                return render(request, 'success.html')
            
        
                
                        if payment_method == 'razorpay':
                            if cart_items:
                                if address_select:
                                    for item in cart_items:
                                        product_id=item.variant_id
                                        quantity=item.quantity
                                        price=item.variant_id.price
                                        t_price=quantity*price
                                        if item.variant_id.catogery_offer_price==0:
                                            t_total=item.variant_id.price * quantity
                                            print(total)
                                        else :
                                            t_total=item.variant_id.catogery_offer_price * quantity
                                            print(total)
                                        print(total)
                                    order = Order(user_id=user, address=selected_address,total_amount=t_total,total_quantity=quantity,varient_Key=product_id,payment_method=payment_method)
                                    order.save()
                                    product_id.quantity -= quantity
                                    product_id.save()
                                    if "coupon" in request.session:
                                        coupon=request.session.get("coupon")
                                        applied=Couponapplied.objects.create(c_code=coupon,c_user=user)
                                        del request.session["coupon"]
                                    client = razorpay.Client(auth=("rzp_test_LKE4UtUkNNR122", "Ma0iVAjSvXm7CJgE5YdgGenB"))
                                    amount = int(subtotal*100) # Replace with the actual order amount
                                    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
                                   
                                    print(payment)
                                    cart_items.delete()
                                    return render(request,'rayzor_main.html',{"amount":amount})    
                            # Replace the following return statement with the appropriate redirect or response
    return render(request, 'home-03.html', {'cart_items': cart_items,
                'first_coupon':first_coupon,
                "catogery_offer_available":catogery_offer_available,
                'total': total,
                "coup":coup,
                'addresses': addresses, 'selected_address': selected_address})

def new_address(request):
    if "name" in request.session:
        user=request.session["name"]
        u_name=Uuser.objects.get(name=user)
        add=Address.objects.filter(user_id=u_name)
        n=[i.address_line for i in add]
        error=None
        k="KERALA"
        if request.method == 'POST':
            address_line = request.POST.get('address_line')
            state = request.POST.get('state')
            district = request.POST.get('district')
            city = request.POST.get('city')
            if  address_line in n:
                error="same address is present enter another"
            elif state!=k:
                error="please enter state as KERALA"
            elif len(district)<3:
                error="please enter a district in kerala"
            elif len(city)<3:
                error="please enter a city in your district"
            if not error:
                new_address = Address(user_id=u_name, address_line=address_line, state=state, district=district, city=city)
                new_address.save()
                return redirect("pro")
            else:
                 return render(request,"address.html",{"error":error})
        return render(request,"address.html")
def profile(request):
    if "name" in request.session:
        li=[]
        user_name = request.session['name']
        user=Uuser.objects.get(name=user_name)
        address=Address.objects.filter(user_id=user)
        for i in address:
         li.append((i.address_line,i.state))
        li=set(li)
        print(li)
        li=list(li)
        return render(request,"profile.html",{"address": address,"user":user,"li":li})
    


def edit_address(request,id):
    if "name" in request.session:
        add = get_object_or_404(Address, id=id)
    if request.method == 'POST':
        add.address_line = request.POST.get('address_line')
        add.state= request.POST.get('state')
        add.district= request.POST.get('district')
        add.city= request.POST.get('city')
        add.save()
        return redirect('pro')
    else:
        context = {'add': add}
        return render(request, 'edit_address.html', context)
    

@never_cache
def cart(request):
    user=None
    if "password" in request.session:
            return redirect('admin_home')
    a = 120
    print(a)
    if 'name' in request.session:
        user_name = request.session['name']
        user = get_object_or_404(Uuser, name=user_name)
        cart_items = CartItem.objects.filter(user_id=user)
        overall_total = 0
        total=0
        for i in cart_items:
            if i.variant_id.catogery_offer_price==0:
                total+=i.variant_id.price * i.quantity
            else :
                total+=i.variant_id.catogery_offer_price * i.quantity
        print(total)
        if request.method == 'POST':
            print('moooooooooooooooooooooooooooo')
            quantity_exceeded = False
            error_messages = []
            qu = 0
            print(quantity_exceeded)
            for cart_item in cart_items:
                product_quantity = cart_item.varient_id.quantity
                cart_id = request.POST.get('cart_id')
                quantity = int(request.POST.get('quantity'))
                product_id = (request.POST.get('varient_id'))
                product = Varient.objects.get(product_id=product_id)
                qu = product.quantity  
                print(qu)
                if cart_item.cart_id == int(cart_id):
                    if qu < quantity:
                        print('helloooooooooooooooooooooooooooooooooooooooo')
                        quantity_exceeded = True
                        error_messages.append({
                            'product_name': cart_item.varient_id.product_key.name,
                            'error_message': 'Quantity exceeds available stock.'
                        })
                    else:
                        print('haiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
                        cart_item.quantity = quantity
                        if  cart_item.varient_id.catogery_offer_price==0:
                            cart_item.sub_total = cart_item.varient_id.price * quantity
                            cart_item.save()
                            # total = sum(item.varient_id.price * item.quantity for item in cart_items)
                            for i in cart_items:
                                total+=i.varient_id.price * i.quantity
                        else:
                            cart_item.sub_total = cart_item.varient_id.catogery_offer_price * quantity
                            cart_item.save()
                            for i in cart_items:
                                total+=i.varient_id.price * i.quantity
                            # total = sum(item.varient_id.catogery_offer_price * item.quantity for item in cart_items)
                        print(total)
                        print(cart_item.quantity, cart_item.sub_total, overall_total)
            if quantity_exceeded:
                return render(request, 'cart.html',{"user":user,'cart_items': cart_items,"user":user, 'error_messages': error_messages})
            else:
                # return redirect(checkout)
                return render(request, 'cart.html',{"user":user,'cart_items': cart_items,"user":user, 'total':total})
        # Replace 'checkout_page' with the appropriate URL name for your checkout page
        return render(request, 'cart.html', {"user":user,'cart_items': cart_items,"user":user,"total":total})
    else:
        guest_cart_items=Guest.objects.all()  
        total=0
        # total = sum(item.guest_variant_id.price * item.guest_quantity for item in guest_cart_items)
        for i in guest_cart_items:
            if i.guest_variant_id.catogery_offer_price==0:
                total+=i.guest_variant_id.price * i.guest_quantity
            else:
                total+=i.guest_variant_id.catogery_offer_price * i.guest_quantity
        for cart_item in guest_cart_items:
            if cart_item.guest_quantity==0:
                cart_item.guest_quantity=1
                cart_item.save()
            if cart_item.guest_variant_id.catogery_offer_price==0:
              cart_item.sub_total = cart_item.guest_variant_id.price * cart_item.guest_quantity
              cart_item.save()
            else:
              cart_item.sub_total = cart_item.guest_variant_id.catogery_offer_price * cart_item.guest_quantity
              cart_item.save()
            # total = sum(item.guest_variant_id.price * item.guest_quantity for item in guest_cart_items)
        return render(request, 'cart.html', {"user":user,'guest_cart_items': guest_cart_items,"total":total})
    #    print("haiiicart")
    #    d=[]
    #    cart=request.session.get("cart_item_data")
    #    if cart:
    #        variant_id=cart.get("variant_id")
    #        quantity=cart.get("quantity")
    #        image=cart.get("image")
    #        name=cart.get("name")
    #        price=cart.get("price")
    #        varient=Varient.objects.get(id=variant_id)
    #        d.append(cart)
    #        print(d)
    #    return render(request, 'cart.html', {"cart":cart,"variant_id":variant_id,"quantity":quantity,"image":image,"price":price})
           
from datetime import datetime, timedelta      
from django.utils import timezone       
from django.http import JsonResponse
def ajaxCoupon(request):
    name = request.session['name']
    user = Uuser.objects.get(name=name)
    cart_items = CartItem.objects.filter(user_id=user)
    item_id = request.GET.get('itemid')
    coupon = request.GET.get('coupon')
    request.session["coupon"]=coupon
    first_coupon = Coupon.objects.all()
    getcoup = Coupon.objects.filter(code=coupon)
    c_amount = 0
    total = 0
    msg="Coupon Applied"
    print("getcoup", getcoup)
    subtotal = sum(item.sub_total() for item in cart_items)
    cuponuser=Couponapplied.objects.all()
    print(cuponuser)
    if cuponuser:
        for i in cuponuser:
            print(i.c_user.name,i.c_code,"user present")
            if i.c_user.name==name:
               if i.c_code==coupon:
                msg="coupon already applied"
                print(msg)
                total=subtotal
                print("haii",i.c_user) 
                  
            else:
                    print("user present but not applied")
                    for i in getcoup:
                        am = i.coupon_minmun_amount
                        print(am)
                        if subtotal > am:
                            total = subtotal - i.coupon_dis_amount  
    else:
        print("user  not present")
        for i in getcoup:
                    am = i.coupon_minmun_amount
                    print(am)
                    if subtotal > am:
                        total = subtotal - i.coupon_dis_amount
                    else:
                        total=subtotal
                        msg=f"coupon is not applicable,minimum purchase amount is {am}"
    
    print("haiii",msg)
    return JsonResponse({"total" : total, "msg" : msg})    


def ajaxCatogery(request):
    name=request.session['name']
    user  = Uuser.objects.get(name=name)
    cart_items = CartItem.objects.filter(user_id=user)
    item_id = request.GET.get('itemid')
    coupon= (request.GET.get('coupon'))
    first_coupon = Coupon.objects.all()
   
    catog=category.objects.get(name=item_id)
    
    total = sum(item.variant_id.price * item.quantity for item in cart_items)
    total=total-catog.catewise_dicount_price
    offer='catogery offer applied'
    return JsonResponse({"total":total,"offer":offer})   

@never_cache
def ajaxQuantity(request):
    if "password" in request.session:
                 return redirect('admin_home')
    if "name" in request.session:
        user_name = request.session['name']
        user = get_object_or_404(Uuser, name=user_name)
        cart_items = CartItem.objects.filter(user_id=user)
        item_id = request.GET.get('itemid')
        quantity = int(request.GET.get('quantity'))
        cart = CartItem.objects.get(cart_id=item_id)
        original_quantity = cart.variant_id.quantity 
        if quantity==0:
            quantity=1
        if quantity > original_quantity:
            return JsonResponse({"error": "Exceeded available quantity."})
        cart.quantity = quantity
        cart.save()
        total_sum=0
        for i in cart_items:
            if i.variant_id.catogery_offer_price==0:
                total_sum+=i.variant_id.price * i.quantity
            else:
                total_sum+=i.variant_id.catogery_offer_price * i.quantity
        # total_sum = sum(item.quantity * item.variant_id.price for item in cart_items)
        total = int(cart.sub_total())
        print(total_sum)
        return JsonResponse({"total": total, "total_sum": total_sum})
    else:
        item_id = request.GET.get('itemid')
        quantity = int(request.GET.get('quantity'))
        cart = CartItem.objects.get(cart_id=item_id)
        original_quantity = cart.variant_id.quantity 
        if quantity==0:
            quantity=1
        if quantity > original_quantity:
            return JsonResponse({"error": "Exceeded available quantity."})
        cart.quantity = quantity
        cart.save()
        total_sum = sum(item.quantity * item.variant_id.price for item in cart_items)
        total = int(cart.sub_total())
        print(total_sum)
        return JsonResponse({"total": total, "total_sum": total_sum})



def ajaxQuantityguest(request):
        cart_items=Guest.objects.all()
        item_id = request.GET.get('itemid')
        quantity = int(request.GET.get('quantity'))
        cart=Guest.objects.get(guest_id=item_id)
        original_quantity = cart.guest_variant_id.quantity 
        if quantity==0:
            quantity=1
        if quantity > original_quantity:
            return JsonResponse({"error": "Exceeded available quantity."})
        cart.guest_quantity = quantity
        cart.save()
        total_sum = sum(item.guest_quantity * item.guest_variant_id.price for item in cart_items)
        print(total_sum)
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


def remove_from_guest_cart(request,item_id):
    if "password" in request.session:
                 return redirect('admin_home')
    item = get_object_or_404(Guest, guest_id=item_id)
    item.delete()
    return redirect('add_to_cart')  # Redirect to the cart page after removing the item
    

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
            category = str(cart_item.variant_id.product_key.catogery)
        coup = Coupon.objects.all()
        add=Address.objects.all()
        for i in add:
            print(i)
        total = sum(item.variant_id.price * item.quantity for item in cart_items)
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
            n=[]
            for item in cart_items:
                quantity = request.POST.get(f"quantity-{item.product_id}")
                n.append(i.item.variant_id.product_key.catogery.catewise_dicount_price)
                print(quantity,'quantity in the cart') 
                if quantity is not None:
                    quantity = int(quantity)
                    item.quantity = quantity
                    item.save()
            if action == 'place_order':
                # Create and save the order
                for item in cart_items:
                        product_id=item.product_id
                    # Process cash on delivery order\
                        quantity=item.quantity
                        price=item.product_id.price
                        t_price=quantity*price
                payment_method = request.POST.get('payment_method')
                if payment_method == 'cash_on_delivery':
                     for item in cart_items:
                        product_id=item.product_id
                    # Process cash on delivery order\
                        quantity=item.quantity
                        price=item.product_id.price
                        t_price=quantity*price
                        order = Order(user_id=user, address=selected_address,total_amount=t_price,total_quantity=quantity,varient_Key=product_id,payment_method=payment_method)
                        order.save()
                        product_id.quantity -= quantity
                        product_id.save()
                    # Replace the following return statement with the appropriate redirect or response
                     return render(request, 'success.html')
                elif payment_method == 'razorpay':
                    for item in cart_items:
                        product_id=item.product_id
                        quantity=item.quantity
                        price=item.product_id.price
                        product_id=item.product_id
                     # Process cash on delivery order\
                        quantity=item.quantity
                        price=item.product_id.price
                        t_price=quantity*price
                        client = razorpay.Client(auth=("rzp_test_LKE4UtUkNNR122", "Ma0iVAjSvXm7CJgE5YdgGenB"))
                        amount = t_price*100  # Replace with the actual order amount
                        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
                        order = Order(user_id=user, address=selected_address, total_amount=t_price,total_quantity=quantity,varient_Key=product_id,payment_method=payment_method)
                        order.save()
                        product_id.quantity -= quantity
                        product_id.save()
                     # Redirect to the Razorpay payment page
                    print(t_price)
                    return render(request,'rayzor_main.html',{'t_price':t_price})
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
            print(i.variant_id.product_key.name,i.sub_total(),i.quantity)
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
            search = request.GET.get('search')
            if search:
                products = Order.objects.filter(id__istartswith=search)
                paginator = Paginator(products, 2)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            else:
                orders = Order.objects.all()
                paginator = Paginator(orders, 5)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            return render(request, 'view_order.html', {"page_obj":page_obj})
  
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
                     qu=Decimal(order.total_quantity)
                     order.varient_Key.quantity+=qu
                     order.varient_Key.save()

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
            qu=Decimal(order.total_quantity)
            order.varient_Key.quantity+=qu
            order.varient_Key.save()
            
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
        coupon_dis_amount= request.POST.get('coupon_dis_amount')
        coupon_minmun_amount = request.POST.get('coupon_minmun_amount')
        valid_from= request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        print(valid_from)
        coup = Coupon.objects.create(
            code =code,
            coupon_dis_amount=coupon_dis_amount,
            coupon_minmun_amount=coupon_minmun_amount,
            valid_from=valid_from,
            valid_to=valid_to
        )
        coup.save()
        return redirect(coupon_view)
    return render(request, 'add_coupon.html')
   else:
    return redirect('admin_login')
   
def change_password(request):
    if "name" in request.session:
        if request.method=="POST":
            error=None
            user_name = request.session['name']
            user = get_object_or_404(Uuser, name=user_name)
            new = request.POST.get('new_password')
            re_new= request.POST.get('re_new_password')
            if new==re_new:
              user.password=re_new
              user.save() 
              return redirect("pro")
            else:
                
                error="not match"
                return render(request,"change_pass.html,",{"error":error})
        else:
            
                user_name = request.session['name']
                user = get_object_or_404(Uuser, name=user_name)
                return render(request,"change_pass.html")



@never_cache
def delivered_products(request):
    if "password" in request.session:
                 return redirect('admin_home')
    if "name"in request.session:
        mes = ''
        name=request.session["name"]
        user=Uuser.objects.get(name=name)
        # Retrieve delivered products from the database
        delivered_product = Order.objects.filter(user_id=user,status='Delivered')
        if request.method == 'POST':
            
            order_id=request.POST.get('order_id')
            # Set an initial empty value for mes
            order=Order.objects.get(id=order_id)
            order.is_returned=True
            order.return_status = 'Pending'
            order.save()
            print(order.is_returned)
            
        return render(request, 'deliverd_pro.html', {"delivered_product":delivered_product,'user': user})
    else:
            # return render(request, 'deliverd_pro.html', {'order': order, 'mes': mes})
     return redirect("loginn")
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
       for i in retn:
        print(i.id)
       return render(request, 'returned_pro.html', {'retn':retn})
    else:
        return redirect("loginn")



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