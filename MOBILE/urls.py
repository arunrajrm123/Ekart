from django.urls import path
from. import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.registerform,name='register'),
    path('otp/<str:otp>/', views.otp_grn, name='verify_otp'),
    path('loginn/',views.loginn,name='loginn'),
    path('user_logout',views.user_logout,name="user_logout"),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('user-list/', views.user_list, name='userlist'),
    path('block-user/<int:id>/', views.block_user, name='blockuser'),
    path('unblock-user/<int:id>/', views.unblock_user, name='unblockuser'),
    path('view_cato/',views.view_category,name='viewcatogery'),
    path('add_cato/',views.add_catogery,name='addcatogery'),
    path('edit_cato/<int:id>/',views.edit_category,name='editcatogery'),
    path('delet/<int:id>', views.delete_category, name='delete_cato'),
    path('edit/<int:product_id>/', views.edit, name='edit'),
    path('product_view/', views.product_view, name='productview'),
    path('add/',views.add_product,name='add'),
    path('delete/<int:product_id>', views.delete_product, name='delete'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='productdetail'),
    path('add_to_cart/', views.cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path(' update_quantity', views. update_quantity, name=' update_quantity'),
    path('home/',views.home,name='home'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('rayzor/', views.razor_pay, name='razor_pay'),
    path('razor_success/', views.razor_success, name='razor_success'),
    path('order/', views.orders, name='orders'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('view-coupon/', views.coupon_view, name='view_coupon'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
    path('change_order_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    # path('return/', views.return_product, name='return_product'),
    path('deli/', views.delivered_products, name='deli'),
    path('v_deli/', views.view_delivered_products, name='v_deli'),
    path('v_retu/', views.view_returned_products, name='v_retu'),
  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)