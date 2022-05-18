from carts.models import CartItem ,Cart

from carts.views import _cart_id

def menu_cart(request):
    #folder 8 video 4  
    try:
        cart =  Cart.objects.get(cart_id = _cart_id(request))
        items = CartItem.objects.filter(cart = cart).count
    except:
        items = 0
    return dict(items=items)
