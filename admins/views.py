from django.shortcuts import render
from django.shortcuts import redirect
from authentication.models import CustomUser
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import get_object_or_404
from django.db.models import Q
from decimal import Decimal
from django.http import HttpResponse
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from authentication.models import *
from carts.models import *
from django.contrib.auth import get_user_model



# Create your views here.

def admin_home(request):
    return render(request,'admins/admin_home.html')

def admin_login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(email=email,password=password)
    
        if user is not None:
            login(request,user)
            print(request.user.is_staff)
            if request.user.is_staff==True:
                return redirect('admin_home')
            else:
                messages.error(request,'Your Email or Password is Incorrect!!')
                return redirect('admin_login')
        else:
            messages.error(request,"Your Email or Password is Incorrect!!")
            return redirect('admin_login')
    return render(request,'admins/admin_login.html')


def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('admin_login')   

def customers(request):
    customers = CustomUser.objects.filter(is_active=True,is_superuser=False)
    context = {
        'data': customers
    }
    return render(request, 'admins/customers.html', context)
def block_user(request,id):
    if request.method=='POST':
        customer = CustomUser.objects.get(pk=id)
        customer.is_active= False
        customer.save()
    return redirect('customers')
    
    
def unblock_user(request,id):
    if request.method=='POST':
        customer = CustomUser.objects.get(pk=id)
        customer.is_active= True
        customer.save()
    return redirect('customers')



def customers(request):
    customer_data = CustomUser.objects.filter(is_superuser=False)
    context = {
        'data': customer_data
    }
    return render(request, 'admins/customers.html', context)

#CATEGORY
def category_list(request):
    brands = ProductBrand.objects.all()
    categories = ProductCategory.objects.all()
    context = {'brands':brands,'categories':categories}
    return render(request, 'admins/category_list.html', context)

def category_add(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        categories = ProductCategory(category_name=category_name)
        categories.save()
        return redirect('category_list')
    return render(request,'admins/category_list.html')

def category_edit(request):
    categories = ProductCategory.objects.all()
    context = {'categories':categories}
    return redirect('category_list',context)



def category_update(request,id):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        categories = ProductCategory(id=id, category_name=category_name)
        categories.save()           
        return redirect('category_list')          
    return render(request, 'admins/category_list.html')

def change_category_block_status(request, id):
    if request.method == 'POST':
        block_status = request.POST.get('block_status', False) == 'True'
        category = ProductCategory.objects.get(pk=id)
        category.is_blocked = block_status
        category.save()
        return redirect('category_list')


def category_delete(request,id):
    categories = ProductCategory.objects.filter(id=id)
    categories.delete()
    context = {'categories':categories}
    return redirect('category_list')


#BRANDS
def brand_list(request):
    brands = ProductBrand.objects.all()
    context = {'brands':brands}
    return render(request, 'admins/brand_list.html',context)

def brand_add(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        brands = ProductBrand(brand_name=brand_name)
        brands.save()
        return redirect('brand_list')
    return render(request,'admins/brand_list.html')

def brand_edit(request):
    brands = ProductBrand.objects.all()
    context = {'brands':brands}
    return redirect('brand_list',context)

def brand_update(request,id):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        brands = ProductBrand(id=id,brand_name=brand_name)
        brands.save()
        return redirect('brand_list')
    return render(request,'admins/brand_list.html')

def change_brand_block_status(request, id):
    if request.method == 'POST':
        block_status = request.POST.get('block_status', False) == 'True'
        brand = ProductBrand.objects.get(pk=id)
        brand.is_blocked = block_status
        brand.save()
        return redirect('brand_list')

def brand_delete(request,id):
    brands = ProductBrand.objects.filter(id=id)
    brands.delete()
    context = {'brands':brands}
    return redirect('brand_list')


#PRODUCT
   
def product_list(request):
    products = Product.objects.all()
    brands=ProductBrand.objects.all()
    categories=ProductCategory.objects.all()
    context = {'products':products,'brands':brands,'categories':categories}
    return render(request, 'admins/product_list.html',context)    



def product_add(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand_id = request.POST.get('product_brand')
        category_id = request.POST.get('product_category')
        product_thumbnail = request.FILES.get('product_thumbnail')
        product_price = request.POST.get('product_price')
        product_description = request.POST.get('product_description')
        product_brand=get_object_or_404(ProductBrand, id=brand_id)
        product_category=get_object_or_404(ProductCategory, id=category_id)
        products = Product(
            product_name = product_name,
            product_brand = product_brand,
            product_category = product_category,
            product_thumbnail = product_thumbnail,
            product_price = product_price,
            product_description = product_description
        )
        products.save()
        return redirect('product_list')
       



def product_edit(request):
    products = Product.objects.all()
    context = {'products':products}
    return redirect('product_list',context)



def product_update(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand_id = request.POST.get('product_brand')
        category_id = request.POST.get('product_category')
        product_price = request.POST.get('product_price')
        product_description = request.POST.get('product_description')
        
        # Retrieve the updated 'product_thumbnail' field value
        product_thumbnail = request.FILES.get('product_thumbnail')
        
        # Update other product details
        product.product_name = product_name
        product.product_brand = get_object_or_404(ProductBrand, id=brand_id)
        product.product_category = get_object_or_404(ProductCategory, id=category_id)
        product.product_price = product_price
        product.product_description = product_description
        
        # Only update 'product_thumbnail' if a new file was provided
        if product_thumbnail:
            product.product_thumbnail = product_thumbnail
        
        # Save the updated product
        product.save()
        
        return redirect('product_list')
    
    return render(request, 'admin/product_list.html', {'product': product})


def product_delete(request,id):
    products = Product.objects.get(id=id)
    brands=ProductBrand.objects.all()
    categories=ProductCategory.objects.all()
    products.delete()
    context = {'products':products,'brands':brands,'categories':categories}
    return redirect('product_list')  

def product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_view.html', {'product': product})


def user_home(request):
    user = CustomUser.objects.all()
    # user = CustomUser.objects.exclude(is_admin=True).order_by('id')
    return render(request,'admins/user_home.html',{'users':user})
# def user_edit(request,id):
#     user = Account.objects.get(id=id)
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         username = request.POST['username']     
#         user = Account.objects.filter(id=id).update(first_name=first_name, last_name=last_name, email=email, username=username)
#         return redirect('user_home')
#     return render(request, 'admin/user_edit.html',{'user':user})

def block_user(request, id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active = False
        user.save()
        return redirect('user_home')  

def unblock_user(request, id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active = True
        user.save()
        return redirect('user_home') 

# def user_search(request):
#     # if 'admin' in request.session:
#     if request.method == 'GET':
#         user_search = request.GET.get('user_search')
#         user = CustomUser.objects.filter(name__icontains=user_search)
#         return render(request,'admins/user_search.html',{'users':user})
#     else:
#         return redirect('user_home')



#addtocart.............................................................addtocart

def order_list(request):
    orders = Order.objects.all().select_related('user','shipping_address').order_by('-order_date')
    order_items = OrderItem.objects.all()
    users = get_user_model().objects.all()
    default_addresses = UserAddress.objects.filter(user__in=users, is_default=True)
    products = Product.objects.all()
    # singleproducts = Product.objects.all()
   
    product_totals = {}
    for order_item in order_items:
        product_total = order_item.quantity * order_item.product.product_price
        product_totals[order_item.id] = product_total
    
    context = {
        'orders': orders,
        'order_items': order_items,
        'users': users,
        'default_addresses': default_addresses,
        'products': products,
        'product_totals': product_totals,
    }
    return render(request, 'admins/oder_list.html',context)  

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
    return render(request, 'admins/oder_list.html')


#coupon.............................................................coupon 
def coupon(request):
    coupons = Coupon.objects.all()
    context = {
        'coupons': coupons
    }
    return render(request, 'admins/coupon.html', context)


def coupon_add(request):
    if request.method == 'POST':
        # Process the form submission and create a new coupon
        coupon_name = request.POST.get('coupon_name')
        code = request.POST.get('code')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        discount_price = request.POST.get('discount_price')
        active = request.POST.get('active')== 'true'
        
        coupon = Coupon.objects.create(
            coupon_name=coupon_name,
            code=code,
            valid_from=valid_from,
            valid_to=valid_to,
            discount_price=discount_price,
            active=active
        )
        coupon.save()
        # Redirect to the coupon list page
        return redirect('coupon')
    return render(request, 'admins/coupon.html')


def coupon_edit(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)

    if request.method == 'POST':
        # Process the form submission and update the coupon
        coupon.coupon_name = request.POST.get('coupon_name')
        coupon.code = request.POST.get('code')
        coupon.valid_from = request.POST.get('valid_from')
        coupon.valid_to = request.POST.get('valid_to')
        coupon.discount_price = request.POST.get('discount_price')
        coupon.active = request.POST.get('active')== 'true'
        coupon.save()
        
        # Redirect to the coupon list page
        return redirect('coupon')
    return render(request, 'admin/coupon.html', {'coupon': coupon})


def coupon_delete(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)

    if request.method == 'POST':
        # Delete the coupon
        coupon.delete()
        
        # Redirect to the coupon list page
        return redirect('coupon')
    return HttpResponse("Invalid Request")








