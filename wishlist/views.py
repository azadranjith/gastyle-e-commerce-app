
# Create your views here.
from django.shortcuts import render,redirect
from store.models import Product, Variation
from .models import Wishlist, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
#adding to cart without logging in
# we use session id as the cart_id while creating cart
    #private fuction to get session id, if session id does not we will create 

def _wish_id(request):
    carti = request.session.session_key
    if not carti:
        cart = request.session.create()
    return carti




# function to add product to cart

def add_wishlist(request, product_id):

    url = request.META.get('HTTP_REFERER')

    product = Product.objects.get(id = product_id)  
    
    try:    
                                                                  #if cart already exist
        # cart = Cart.objects.get(cart_id = _cart_id(request))
        wishlist = Wishlist.objects.get(wishlist_id = _wish_id(request))

    except Wishlist.DoesNotExist: 

        wishlist = Wishlist.objects.create(wishlist_id = _wish_id(request))    #creates a cart 

    wishlist.save()
    
    if request.user.is_authenticated:
        # cart_item_exists = CartItem.objects.filter(product=product,user=request.user).exists()
        wishlist_item_exists = WishlistItem.objects.filter(product=product,user=request.user).exists()

    else:
        # cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
        wishlist_item_exists = WishlistItem.objects.filter(product=product,wishlist=wishlist).exists()

    if wishlist_item_exists:

         #for the user specific cart_item
        if request.user.is_authenticated:
            
            # cart_item = CartItem.objects.filter(product = product,user=request.user)
            wishlist_item = WishlistItem.objects.filter(product = product,user=request.user)
        else:
            # cart_item = CartItem.objects.filter(product = product,cart = cart)
            wishlist_item = WishlistItem.objects.filter(product = product,wishlist=wishlist)


        # else:
        #     if request.user.is_authenticated:
        #         item = WishlistItem.objects.create(product = product,user=request.user)
        #     #make new cartitem  
        #     else:
        #         item = WishlistItem.objects.create(product = product,wishlist = wishlist)

        #     if len(product_variation) > 0:
        #         item.variations.clear()
        #         item.variations.add(*product_variation)
        #     item.save()
    else:
        if request.user.is_authenticated:
            item = WishlistItem.objects.create(product = product,user=request.user) 
        else:        
            item = WishlistItem.objects.create(product = product,wishlist = wishlist)# q=1 bcz we are adding and creating it for the first time
        # if len(product_variation) > 0:
        #     item.variations.clear()
        #     item.variations.add(*product_variation)
        item.save() #should i move this???????????
    
    return redirect(url) 


def wishlist(request,wishlist_items = None): 
    try:
        if request.user.is_authenticated:
            wishlist_items = WishlistItem.objects.filter(user=request.user).order_by('id')
        else:
            wishlist = Wishlist.objects.get(wishlist_id=_wish_id(request))

            wishlist_items = WishlistItem.objects.filter(wishlist = wishlist).order_by('id')

    except ObjectDoesNotExist:
        pass

    context = {
        'wishlist_items':wishlist_items
    }

    return render(request,'wishlist/wishlist.html',context)  

def remove_wishlist(request,wishlist_item_id):
    url = request.META.get('HTTP_REFERER')
    try:
        wishlist_item = WishlistItem.objects.get(id=wishlist_item_id)
        wishlist_item.delete()
    
    except ObjectDoesNotExist:
        pass
    return redirect(url)  


