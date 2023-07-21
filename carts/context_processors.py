from .models import Cart,CartItem
from .views import _cart_id
from .models import Wishlist



def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return{}
    else:
        try:
            cart =Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
                
            else:    
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count = cart_count)     


def wishlist_counter(request):
    wishlist_count = 0
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_count = wishlist.products.count()
        except Wishlist.DoesNotExist:
            pass
    return {'wishlist_count': wishlist_count}