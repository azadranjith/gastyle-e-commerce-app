


from django.utils.text import slugify
from accounts.models import Account
from orders.views import payment

from store.models import Product, Variation

from orders.models import Order, OrderProduct, Payment
from store.views import product_detail

from .forms import CategoryForm, ProductForm, OrderForm,VariationForm

from category.models import Category
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





# @login_required(login_url='admi_login')  
def admin_home(request):
    user_data = Account.objects.all()

    context = {
        'user_data':user_data
    }

    return render(request,'admin/admi_home.html',context)

# @login_required(login_url='admi_login')  
def product_data(request):
    product_data = Product.objects.all()

    context = {
        'product_data':product_data
    }

    return render(request,'admin/product_data.html',context)
# @login_required(login_url='admi_login')  
def order_data(request):
    order_data = Order.objects.filter(is_ordered = True)
    unpayed_order = Order.objects.filter(is_ordered = False)
    unpayed_order.delete()
    context = {
        'order_data':order_data  
    }

    return render(request,'admin/order_data.html',context)
# @login_required(login_url='admi_login')  
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
# @login_required(login_url='admi_login')  
def add_product(request):
    product_form = ProductForm(initial={'slug': 'no need'})
    if request.method == 'POST':
        product_name = request.POST['product_name']

        slug = slugify(product_name)
        product_form = ProductForm(request.POST,request.FILES)  

        
        if product_form.is_valid():
            
            
        
            product_form.save()
    

            messages.success(request,'Producte has been added')

            product_detail = Product.objects.get(product_name = product_name)
            
            product_detail.slug = slug
            product_detail.save()  
            product_form = ProductForm(instance=product_detail)   
            context = {
            'product_detail':product_detail,
            'product_form':product_form
            }
            return render(request,'admin/edit_product.html',context)  

    context = {
        
        'product_form':product_form
    }

    return render(request,'admin/add_product.html',context)    
@login_required(login_url='admi_login')  
def remove_product(request,product_id):

    product = Product.objects.get(id=product_id)

    product.delete()

    return redirect('product_data')

@login_required(login_url='admi_login')
def block_user(request,user_id):

    user = Account.objects.get(id = user_id)

    user.is_active = False

    user.save()

    return redirect('admi_home')
@login_required(login_url='admi_login')
def unblock_user(request,user_id):

    user = Account.objects.get(id = user_id)

    user.is_active = True

    user.save()

    return redirect('admi_home')


#CATEGORIES 

def categories(request):

    cat = Category.objects.all()
    context = {
        'category':cat,
    }
    return render(request,'admin/categories.html',context)  

def remove_cat(request,cat_id):

    cat = Category.objects.get(id=cat_id)

    cat.delete()

    return redirect('categories') 

def add_category(request):
    category_form = CategoryForm(initial={'slug': 'no need'})
    if request.method == 'POST':
        
        category_name = request.POST['category_name']


        slug = slugify(category_name)  
        category_form = CategoryForm(request.POST,request.FILES) 

        if category_form.is_valid():
               
            category_form.save()



            messages.success(request,'Producte has been added')
            # return redirect('edit_product') 
            category_detail = Category.objects.get(category_name = category_name)
            
            category_detail.slug = slug
            category_detail.save()    
            product_form = ProductForm(instance=category_detail)   
            context = {
            'category_detail':category_detail,
            'product_form':product_form
            }
            return render(request,'admin/edit_category.html',context)     
    
    context = {
        
        'category_form':category_form
    }
    return render(request,'admin/add_category.html',context)  

def edit_category(request,category_id):

    category_detail = Category.objects.get(id = category_id)

    if request.method == 'POST':

        category_form = CategoryForm(request.POST,request.FILES,instance=category_detail)

        if category_form.is_valid():
            
        
            category_form.save()
    

            messages.success(request,'Producte has been updated')
            # return redirect('edit_product') 
    else:
        category_form = CategoryForm(instance=category_detail) 
    context = {
        'category_detail':category_detail,
        'category_form':category_form
    }

    return render(request,'admin/edit_category.html',context)  




def edit_order(request,order_number):
    order = Order.objects.get(order_number=order_number)
    
    if request.method == 'POST':
        print('method is post')
        status = request.POST['status']
        print(status)
        
        order.status = status
        order.save()  
    
    order = Order.objects.get(order_number=order_number)
    order_form = OrderForm(instance = order) 
    order_detail = OrderProduct.objects.filter(order=order)
    print("order is " ,order_detail) 
    payment = Payment.objects.get(id = order.payment.id) 
    print("order is " ,order)     
       #########################

    subtotal = 0 
    for i in order_detail:
        
        subtotal += i.product_price * i.quantity 

    context = {
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal,
        'payment':payment,
        'order_form':order_form,
    }
    # return render(request,'accounts/order_detail.html',context)  
    return render(request,'admin/edit_order.html',context)  


def remove_order(request,order_number):

    cat = Order.objects.get(order_number=order_number)

    cat.delete()

    return redirect('order_data') 

def add_variations(request,product_id):
    variation_form = VariationForm()
    product = Product.objects.get(id = product_id)
    if request.method == 'POST':
        
        variation_form = VariationForm(request.POST,request.FILES) 

        
        if variation_form.is_valid():
            
            
        
            variation_form.save()
    

            messages.success(request,'Producte has been added')

            # variation_detail = Variation.objects.get(product = product)
            
              
            # variation_form = VariationForm(instance=variation_detail)   
            # context = {
            # 'product_detail':product_detail,
            # 'product_form':product_form
            # }
            # return render(request,'admin/edit_product.html',context)  

    context = {
        
        'variation_form':variation_form,
        'product_id':product_id,

    }
    return render(request,'admin/add_variations.html',context)