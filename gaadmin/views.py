from django.shortcuts import render

from accounts.models import Account

from store.models import Product

from orders.models import Order
# Create your views here.
def admin_home(request):
    user_data = Account.objects.all()

    context = {
        'user_data':user_data
    }

    return render(request,'admin/admi_home.html',context)


def product_data(request):
    product_data = Product.objects.all()

    context = {
        'product_data':product_data
    }

    return render(request,'admin/product_data.html',context)

def order_data(request):
    order_data = Order.objects.all()

    context = {
        'order_data':order_data  
    }

    return render(request,'admin/order_data.html',context)
    