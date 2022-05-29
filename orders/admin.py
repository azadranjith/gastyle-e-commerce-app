from django.contrib import admin

# Register your models here.
from .models import Order,OrderProduct,Payment

#to display cleanly at django admin write OrderAdmin --- not done lecture 18 video 1

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)
