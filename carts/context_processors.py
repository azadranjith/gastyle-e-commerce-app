from carts.models import CartItem ,Cart

from carts.views import _cart_id

def menu_cart(request):#somthing here while admin comes
    #folder 8 video 4  
    try:
        cart =  Cart.objects.filter(cart_id = _cart_id(request))
        if request.user.is_authenticated:
            items = CartItem.objects.all().filter(user=request.user)
        else:

            items = CartItem.objects.all().filter(cart = cart[:1])
        count = 0
        for item in items:
            count += 1

        items = count

    except:
        items = 0
    return dict(items=items)
