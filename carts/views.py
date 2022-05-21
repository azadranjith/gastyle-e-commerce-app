
from django.shortcuts import render,redirect
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.http import HttpResponse
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

    product = Product.objects.get(id = product_id)  
    product_variation = []
    if request.method == 'POST':
        
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact = key,variation_value__iexact = value)#this is to check the fields entered are matching with database and iexact is to ignore the case sensitivity while comparing
                product_variation.append(variation)
            except:
                print("hopless")

         
        


              #to get the product added to the cart
    try:    
                                                                  #if cart already exist
        cart = Cart.objects.get(cart_id = _cart_id(request))

    except Cart.DoesNotExist: 

        cart = Cart.objects.create(cart_id = _cart_id(request))    #creates a cart 

        cart.save()
    # created the cart and got the product

    
    # add product to cart, ie TO CartItem ---------combine the product and cart

    cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
    if cart_item_exists:
        cart_item = CartItem.objects.filter(product = product,cart = cart)
            #variations already in database

            #current variations ie submitted form ---will get from product_variation list

            #we need item_id --from datebase

    #existing_variation will be multiple so we need a list
        ex_var_list = []
        id = [] #to store id's of cart item
    #check is current variation in existing variation 
        for item in cart_item: #looping through each cartitem
            existing_variation = item.variations.all() #this existing_variation is a query set need to make it to list
            ex_var_list.append(list(existing_variation)) #
            id.append(item.id) #now we have id list here 
        if product_variation in ex_var_list: 

            #increase quantity
                #find the cart with id
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product,id=item_id)
            item.quantity += 1
            item.save()
        else:
            #make new cartitem  
            item = CartItem.objects.create(product = product,cart = cart,quantity = 1)

            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:

        item = CartItem.objects.create(product = product,cart = cart,quantity = 1) # q=1 bcz we are adding and creating it for the first time
        if len(product_variation) > 0:
            item.variations.clear()
            item.variations.add(*product_variation)
        item.save()
    
    return redirect('cart')

def cart(request,total = 0,quantity = 0,cart_items = None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True).order_by('id')
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