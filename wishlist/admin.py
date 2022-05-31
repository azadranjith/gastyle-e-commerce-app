from django.contrib import admin

# Register your models here.

from .models import WishlistItem, Wishlist


admin.site.register(Wishlist)

admin.site.register(WishlistItem)