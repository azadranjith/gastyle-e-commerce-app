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
    path('block_user/<int:user_id>',views.block_user,name = 'block_user'),
    path('unblock_user/<int:user_id>',views.unblock_user,name = 'unblock_user'),  


    #category

    path('categories/',views.categories,name='categories'),
    path('remove_cat/<int:cat_id>',views.remove_cat,name = 'remove_cat'), 
    path('add_category/',views.add_category,name = 'add_category'), 
    path('edit_category/<int:category_id>/',views.edit_category,name='edit_category'),  

    #order
    path('edit_order/<int:order_number>',views.edit_order,name='edit_order'),
    path('remove_order/<int:order_number>',views.remove_order,name = 'remove_order'), 

    #edit variation

    path('add_variations/<int:product_id>',views.add_variations,name = 'add_variations'), 



]       