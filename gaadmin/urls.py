from django.urls import path

from . import views

urlpatterns = [
    path('',views.admin_home,name='admi_home'),
    path('product_data/',views.product_data,name='product_data'),
    path('order_data/',views.order_data,name='order_data'),
]   