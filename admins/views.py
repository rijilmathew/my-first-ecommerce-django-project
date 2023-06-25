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

from .models import *
from authentication.models import *



# Create your views here.

def admin_home(request):
    return render(request,'admins/admin_home.html')


def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')   

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

def search(request):
    if 'keyword' in request.GET:
        keyword =request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_description__icontains=keyword)|Q(product_name__icontains=keyword))#_icontains means it look for the whole description and if it found  anything related to the product then it will return the product
            product_count = products.count()
    context = {
        'products': products,
        'product_count':product_count,
    }
    return render(request, 'store/store.html', context)

 #USER

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


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        price = request.POST.get('price')

        try:
            decimal_price = Decimal(price)
        except (InvalidOperation, TypeError):
            # Handle the case where the price is not a valid decimal
            # You can return a JSON response with an error message
            return JsonResponse({'message': 'Invalid price'}, status=400)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        # Check if the cart item already exists
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, price=decimal_price)
        if not created:
            # Increment the quantity
            cart_item.quantity += 1
            cart_item.save()

        # Update the cart total
        cart.total += decimal_price
        cart.save()

        # Return a success JSON response
        return JsonResponse({'message': 'Item added to cart successfully'})

    # Return a JSON response for unsupported methods
    return JsonResponse({'message': 'Method not allowed'}, status=405)






