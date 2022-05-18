from django.contrib import admin

from carts.models import CartItem, Cart

# Register your models here.

admin.site.register(Cart)

admin.site.register(CartItem)
