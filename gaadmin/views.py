
from django.utils.text import slugify
from accounts.models import Account

from store.models import Product

from orders.models import Order
from store.views import product_detail

from .forms import ProductForm
# Create your views here.


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.contrib import auth 

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


@never_cache
def admi_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None and user.is_admin:
            
        
            auth.login(request,user)     
           
            return redirect('admi_home')   

        else:
            messages.error(request,'invalid login credentials')
            return redirect('admi_login')  
    return render(request,'admin/login.html')

@login_required(login_url='admi_login')
@never_cache
def admi_logout(request):  
    auth.logout(request)
    messages.success(request,'you are logged out ')
    return redirect('admi_login')





@login_required(login_url='admi_login')  
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

def edit_product(request,product_id):

    product_detail = Product.objects.get(id = product_id)

    if request.method == 'POST':

        product_form = ProductForm(request.POST,request.FILES,instance=product_detail)

        if product_form.is_valid():
            
        
            product_form.save()
    

            messages.success(request,'Producte has been updated')
            # return redirect('edit_product') 
    else:
        product_form = ProductForm(instance=product_detail) 
    context = {
        'product_detail':product_detail,
        'product_form':product_form
    }

    return render(request,'admin/edit_product.html',context)  

def add_product(request):
    product_form = ProductForm()
    if request.method == 'POST':
        product_name = request.POST['product_name']

        slug = slugify(product_name)
        product_form = ProductForm(request.POST,request.FILES)  

        
        if product_form.is_valid():
            
            
        
            product_form.save()
    

            messages.success(request,'Producte has been added')
            # return redirect('edit_product')   
    
    context = {
        
        'product_form':product_form
    }

    return render(request,'admin/add_product.html',context)    

def remove_product(request,product_id):

    product = Product.objects.get(id=product_id)

    product.delete()

    return redirect('product_data')
