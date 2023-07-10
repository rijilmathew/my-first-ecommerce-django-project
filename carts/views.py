
from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from admins.models import Product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required
from authentication.models import UserAddress
from carts.models import Order,OrderItem
from django.contrib import messages
import random
import string
from .models import Wishlist
from admins.models import Coupon
from django.utils import timezone
from django.http import JsonResponse






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
            if cart_item.quantity < product.product_quantity:
                cart_item.quantity += 1
                cart_item.save()
        except CartItem.DoesNotExist:
            if product.product_quantity >0:
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
            if cart_item.quantity < product.product_quantity:
                cart_item.quantity += 1
                cart_item.save()
        except CartItem.DoesNotExist:
            if product.product_quantity >0:
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
        grand_total = total   
       
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


from django.shortcuts import get_object_or_404

def checkout(request):
    # Retrieve active coupons
    coupons = Coupon.objects.filter(active=True)

    # Retrieve user addresses
    addresses = Order.objects.filter(user=request.user).values(
        'fname', 'lname', 'email', 'phone', 'address', 'city', 'state', 'pincode'
    ).distinct()

    # Initialize variables
    total = 0
    quantity = 0
    
    grand_total = 0
    cart_items = None
    applied_coupon = None

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    # Calculate total, quantity, and tax
    for cart_item in cart_items:
        total += cart_item.product.product_price * cart_item.quantity
        quantity += cart_item.quantity


    grand_total = total

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')

        if coupon_code:
            applied_coupon = get_object_or_404(Coupon, code=coupon_code, active=True)

            # Check if coupon is within its validity period
            if applied_coupon.valid_from <= timezone.now().date() <= applied_coupon.valid_to:
                request.session['applied_coupon'] = coupon_code
                grand_total -= applied_coupon.discount_price
                grand_total = max(0, grand_total)  # Ensure grand_total is not negative

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'total':total,
        'grand_total': grand_total,
        'addresses': addresses,
        'coupons': coupons,
        'applied_coupon': applied_coupon,
    }

    return render(request, 'layouts/checkout.html', context)

from django.shortcuts import redirect

def placeorder(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_method = request.POST.get('payment_mode')
        
        # Calculate total, quantity, tax, and grand_total
        total = 0
        quantity = 0
        
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.product_price * cart_item.quantity
            quantity += cart_item.quantity
        

        grand_total = total
        
        neworder.total_mrp = grand_total
        neworder.discount_amount = Coupon.discount_price
        
        # Apply coupon if available
        if 'applied_coupon' in request.session:
            coupon_code = request.session['applied_coupon']
            applied_coupon = Coupon.objects.get(code=coupon_code)
            
            if applied_coupon.active and applied_coupon.valid_from <= timezone.now().date() <= applied_coupon.valid_to:
                neworder.coupon = applied_coupon
                discount_amount = applied_coupon.discount_price 
                neworder.discount_amount = discount_amount
                grand_total -= discount_amount
        
        neworder.payment_amount = grand_total
        
        neworder.save()
        
        # Create OrderItem instances for each cart item
        for cart_item in cart_items:
            OrderItem.objects.create(
                order_no=neworder,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            
            # Decrease the product quantity
            product = cart_item.product
            product.product_quantity -= cart_item.quantity
            product.save()
        
        # Clear the cart and applied coupon after placing the order
        CartItem.objects.filter(user=request.user, is_active=True).delete()
        request.session.pop('applied_coupon', None)
        
        # Redirect to the Order Summary page with the newly created Order's ID
        return redirect('order_summary', order_id=neworder.id)

    return redirect('/')











# def placeorder(request):
#     if request.method == 'POST':
#         neworder = Order()
#         neworder.user = request.user
#         neworder.fname = request.POST.get('fname')
#         neworder.lname = request.POST.get('lname')
#         neworder.email = request.POST.get('email')
#         neworder.phone = request.POST.get('phone')
#         neworder.address = request.POST.get('address')
#         neworder.city = request.POST.get('city')
#         neworder.state = request.POST.get('state')
#         neworder.pincode = request.POST.get('pincode')
#         neworder.payment_method = request.POST.get('payment_mode')
        

#         # Calculate total, quantity, tax, and grand_total
#         total = 0
#         quantity = 0
#         tax = 0
#         grand_total = 0
#         cart_items = None
        
#         cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         for cart_item in cart_items:
#             total += cart_item.product.product_price * cart_item.quantity
#             quantity += cart_item.quantity
        
#         tax = (2 * total) / 100
#         grand_total = total + tax
       

#         neworder.total_mrp = grand_total
        
#         neworder.save()
#         # Create OrderItem instances for each cart item
#         for cart_item in cart_items:
#             OrderItem.objects.create(
#                 order_no=neworder,
#                 product=cart_item.product,
#                 quantity=cart_item.quantity,
                
#             )
#             # Decrease the product quantity
#             product = cart_item.product
#             product.product_quantity -= cart_item.quantity
#             product.save()
#         # Clear the cart after placing the order
#         CartItem.objects.filter(user=request.user, is_active=True).delete()
        
#     # Redirect to the Order Summary page with the newly created Order's ID
#     # messages.success(request, 'Your order has been placed successfully.')
#     # return redirect('order_summary', order_id=order.id)
#     return redirect('/')


       
        
    

@login_required(login_url='user_login')
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    default_address = UserAddress.objects.filter(user=request.user, is_default=True).first()
    shipping_address = order.shipping_address
    order_items = OrderItem.objects.filter(order_no=order)

    context = {
        'order': order,
        'order_items': order_items,
        'default_address': default_address,
        'shipping_address': shipping_address
    }

    return render(request, 'layouts/order_summary.html', context)
def order_edit(request):
    orders = Order.objects.all()
    context = {'orders':orders}
    return redirect('order_list', context)

def order_update(request,id):
    order_status = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        status = request.POST.get('order_status')
        order_status.order_status = status
        order_status.save()
        return redirect('order_list')
    return render(request, 'admin/order_list.html')

@login_required(login_url='user_login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    context = {
        'orders': orders
    }
    return render(request, 'layouts/order_history.html', context)


def vieworder(request, od_no):
    order = Order.objects.filter(order_no=od_no, user=request.user).first()
    order_items = OrderItem.objects.filter(order_no=order)
    
    shipping_address = {
        'fname': order.fname,
        'lname': order.lname,
        'email': order.email,
        'phone': order.phone,
        'address': order.address,
        'city': order.city,
        'state': order.state,
        'pincode': order.pincode,
    }
    
    context = {
        'order': order,
        'order_items': order_items,
        'shipping_address': shipping_address
    }

    return render(request, 'layouts/vieworder.html', context)



    



@login_required(login_url='user_login')
def add_to_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        product = Product.objects.get(id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(product)
    return redirect('wishlist')


@login_required(login_url='user_login')
def wishlist_view(request):
    try:
        wishlist = Wishlist.objects.get(user=request.user)
    except Wishlist.DoesNotExist:   
        wishlist = None

    context = {
        'wishlist': wishlist,
    }
    return render(request, 'layouts/wishlist.html', context)
