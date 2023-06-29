from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from admins.models import Product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required
from authentication.models import UserAddress



# Create your views here.



def _cart_id(request):  # private fun for getting the cart id
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)

    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(user=current_user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=current_user)

        try:
            cart_item = CartItem.objects.get(product=product, user=current_user, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                user=current_user,
            )

        return redirect('cart')
    
    else:
        cart_id = _cart_id(request)
        try:
            cart = Cart.objects.get(cart_id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=cart_id)
        
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
        
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
   
    product = get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
           cart_item = CartItem.objects.get(product=product,user=request.user, id=cart_item_id)
        else:
             cart = Cart.objects.get(cart_id=_cart_id(request))
             cart_item = CartItem.objects.get(product=product,cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')
def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
       cart_item = CartItem.objects.get(product=product,user=request.user, id = cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
     
def cart(request, total=0, quantity=0, cart_items=None):

    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
             cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:     
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity)
            quantity += cart_item.quantity
        tax= (2*total)/100
        grand_total = total+ tax    
       
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total'     : total,
        "quantity"  : quantity,
        'cart_item' : cart_items,
        'tax'       : tax,
        'grand_total': grand_total  
        
       
      
    }
    
    return render(request, 'layouts/cart.html',context)

# @login_required
# def checkout(request,total=0, quantity=0, cart_items=None):
#     default_address = UserAddress.objects.filter(user=request.user, is_default=True).first()
#     addresses = UserAddress.objects.filter(user=request.user)
#     try:
#         tax=0
#         grand_total=0
#         if request.user.is_authenticated:
#              cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         else:     
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.product_price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax= (2*total)/100
#         grand_total = total+ tax    
       
#     except ObjectDoesNotExist:
#         pass
    
#     context = {
#         'total'     : total,
#         "quantity"  : quantity,
#         'cart_item' : cart_items,
#         'tax'       : tax,
#         'grand_total': grand_total  
        
       
      
#     }
#     return render(request, 'layouts/checkout.html',context, {'default_address': default_address, 'addresses': addresses})


@login_required(login_url='user_login')
def checkout(request):
    default_address = UserAddress.objects.filter(user=request.user, is_default=True).first()
    addresses = UserAddress.objects.filter(user=request.user)
    try:
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0
        cart_items = None
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += cart_item.product.product_price * cart_item.quantity
            quantity += cart_item.quantity
        
        tax = (2 * total) / 100
        grand_total = total + tax
    
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'default_address': default_address,
        'addresses': addresses,
    }
    
    return render(request, 'layouts/checkout.html', context)


