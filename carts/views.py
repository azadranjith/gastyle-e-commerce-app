from django.shortcuts import render,redirect
from store.models import Product
from carts.models import Cart, CartItem
# Create your views here.

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
    product = Product.objects.get(id = product_id)                #to get the product added to the cart
    try:    
                                                                  #if cart already exist
        cart = Cart.objects.get(cart_id = _cart_id(request))

    except Cart.DoesNotExist: 

        cart = Cart.objects.create(cart_id = _cart_id(request))    #creates a cart 

        cart.save()
    # created the cart and got the product

    
    # add product to cart, ie TO CartItem ---------combine the product and cart
    try:
        cart_item = CartItem.objects.get(product = product, cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:

        cart_item = CartItem.objects.create(product = product,cart = cart,quantity = 1) # q=1 bcz we are adding and creating it for the first time

        cart_item.save()
    print(cart_item.quantity)
    return redirect('cart')

def cart(request,total = 0,quantity = 0,cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (3 * total)/100
        grand_total = total + tax
    except :  
        total = 0
        quantity = 0
        cart_items = 0
        tax=0
        grand_total=0
    
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
    
    except ObjectNotExist:
        pass
    return redirect('cart')

def remove_item(request,cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        
    
    except ObjectNotExist:
        pass

    return redirect('cart')