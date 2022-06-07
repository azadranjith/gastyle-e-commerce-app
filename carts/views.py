
from django.shortcuts import render,redirect
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.http import HttpResponse

from django.contrib import messages

from django.contrib.auth.decorators import login_required
#adding to cart without logging in
# we use session id as the cart_id while creating cart
    #private fuction to get session id, if session id does not we will create 

def _cart_id(request):
    carti = request.session.session_key
    if not carti:
        cart = request.session.create()
    return carti




# function to add product to cart

def add_cart(request, product_id):
    stock = "" 
    product = Product.objects.get(id = product_id)
    var = []
      
    variation = Variation.objects.filter(product=product)
    for i in variation:
        var.append(i)
        
    print(var)
    product_variation = []
    product_variation.append(var[0])
    product_variation.append(var[-1])
    
    if request.method == 'POST':
        product_variation = []
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact = key,variation_value__iexact = value)#this is to check the fields entered are matching with fields database and iexact is to ignore the case sensitivity while comparing
                product_variation.append(variation)
            except:
                print("hopless")

    print("product variation list   :",product_variation)    

              #to get the product added to the cart
    try:    
                                                                  #if cart already exist
        cart = Cart.objects.get(cart_id = _cart_id(request))

    except Cart.DoesNotExist: 

        cart = Cart.objects.create(cart_id = _cart_id(request))    #creates a cart 

    cart.save()
    # created the cart and got the product

    
    # add product to cart, ie TO CartItem ---------combine the product and cart

    #for the user specific cart_item
    if request.user.is_authenticated:
        cart_item_exists = CartItem.objects.filter(product=product,user=request.user).exists()

    else:
        cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()

    if cart_item_exists:

         #for the user specific cart_item
        if request.user.is_authenticated:

            cart_item = CartItem.objects.filter(product = product,user=request.user)
        else:
            cart_item = CartItem.objects.filter(product = product,cart = cart)



            #variations already in database in specific to this cart

            #current variations ie submitted form ---will get from product_variation list

            #we need id of each existing cart_item--from datebase

    #existing_variation will be multiple so we need a list
        ex_var_list = []
        id = [] #to store id's of cart item
    #check is current variation in existing variation 
        for item in cart_item: #looping through each cartitem
            existing_variation = item.variations.all() #this existing_variation is a query set need to make it to list
            ex_var_list.append(list(existing_variation)) #
            id.append(item.id) #now we have id list here 

        print("existing list   :",ex_var_list)   
        print("cartitem index   :",id) 

        #######################    
        if product_variation in ex_var_list: 

            #increase quantity
                #find the cart with id
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product,id=item_id)
            item.quantity += 1
            
            item.save()
           


        else:
            if request.user.is_authenticated:
                item = CartItem.objects.create(product = product,user=request.user,quantity = 1)
            #make new cartitem  
            else:
                item = CartItem.objects.create(product = product,cart = cart,quantity = 1)

            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        if request.user.is_authenticated:
            item = CartItem.objects.create(product = product,user=request.user,quantity = 1)
        else:        
            item = CartItem.objects.create(product = product,cart = cart,quantity = 1) # q=1 bcz we are adding and creating it for the first time
        if len(product_variation) > 0:
            item.variations.clear()
            item.variations.add(*product_variation)
        item.save() #should i move this???????????
    print(product_variation)  
    return redirect('cart')

def cart(request,total = 0,quantity = 0,cart_items = None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user).order_by('id')
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))

            cart_items = CartItem.objects.filter(cart=cart).order_by('id')#deleted the is_active filter
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (3 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:  
        pass
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }

    return render (request,'store/cart.html',context) 

# removing cart_item
#differnt from tuturail this works fine
def remove_cart(request,cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
    
    except ObjectDoesNotExist:
        pass
    return redirect('cart')

def remove_item(request,cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        
    
    except ObjectDoesNotExist:
        pass

    return redirect('cart')

@login_required(login_url='login')#when not loged in redircted to login_url and the url will have next keyword
def checkout(request,total = 0,quantity = 0,cart_items = None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True).order_by('id')#do really need is_active for cartitem??
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True).order_by('id')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

            if cart_item.quantity > cart_item.product.stock:
                messages.error(request,f"{cart_item.product.product_name} exceeds stock limit ")
                messages.success(request,f"only {cart_item.product.stock} is avaliable")
                return redirect('cart') 

        tax = (3 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:  
        pass

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
        }
    return render (request,'store/checkout.html',context)    