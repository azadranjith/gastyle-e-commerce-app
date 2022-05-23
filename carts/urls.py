from django.urls import path

from . import views


urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),
    path('remove_item/<int:cart_item_id>/',views.remove_item,name = 'remove_item'),
    path('checkout/',views.checkout,name='checkout'),
] 