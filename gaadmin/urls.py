from django.urls import path

from . import views

urlpatterns = [
    path('',views.admi_login,name='admi_login'),
    path('admin_home/',views.admin_home,name='admi_home'),
    path('product_data/',views.product_data,name='product_data'),
    path('order_data/',views.order_data,name='order_data'),
    path('edit_product/<int:product_id>/',views.edit_product,name='edit_product'),
    path('admi_logout/',views.admi_logout,name = 'admi_logout'),
    path('add_product/',views.add_product,name = 'add_product'),
    path('remove_product/<int:product_id>',views.remove_product,name = 'remove_product'),      

]       