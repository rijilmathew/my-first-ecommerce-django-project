from django.shortcuts import render,redirect
from admins.models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from carts.models import CartItem,Wallet
from carts.views import _cart_id  
from admins.models import Filter_Price
from decimal import Decimal










# Create your views here.

def index(request):
    context = {}
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(product_name__icontains=q) | Q(product_description__icontains=q))
        products = Product.objects.filter(multiple_q)
        context['products'] = products
    else:

        best_products = Product.objects.filter(best_product=True)[:3]  # Fetch the first three best products
        new_arrivals = Product.objects.filter(new_arrival=True) # Fetch the first three new arrival products
        context['best_products'] = best_products
        context['new_arrivals'] = new_arrivals
        

    return render(request, 'layouts/index.html', context)        








def product_home(request):
    category = request.GET.get('category')
    filter_price = request.GET.get('price')
    context = {}

    if category is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(product_category__category_name=category)
    if filter_price:
        products = products.filter(filter_price__price=filter_price)

    # Pagination
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    categories = ProductCategory.objects.all()
    brands = ProductBrand.objects.all()
    filter_prices = Filter_Price.objects.all()
   
    context = {
        'products': products,
        'brands': brands,
        'categories': categories,
        'selected_category': category, # Pass the selected category to the template
        'selected_price_filter': filter_price,
        'filter_prices': filter_prices,
    }

   

    return render(request, 'layouts/collections.html', context)






# def product_by_brand(request,id):
#     products = Product.objects.filter(product_brand = id)
#     categories = ProductCategory.objects.all()
#     brands = ProductBrand.objects.all()
#     context = {
#         'products':products,
#         'categories':categories,
#         'brands':brands,
#     }
#     return render(request,'layouts/product_by_brand.html',context)

# def product_by_category(request, id):
#     products = Product.objects.filter(product_category=id)
#     categories = ProductCategory.objects.all()
#     brands = ProductBrand.objects.all()
#     context = {
#         'products': products,
#         'categories': categories,
#         'brands': brands,
#     }
#     return render(request, 'layouts/product_by_category.html', context)






def single_product(request, id):
    product = get_object_or_404(Product, id=id)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product = product).exists()
   
    context = {
        'product': product,
        'in_cart': in_cart
    }
    return render(request, 'layouts/single_product.html', context)



   


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        products = Product.objects.order_by('-created_at').filter(
            Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword)
        )

        paginator = Paginator(products, 2)  # Adjust the page size as needed
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        context = {
            'products': products,
            'product_count': paginator.count,
            'keyword': keyword,
        }
    
    return render(request, 'layouts/collections.html', context)


@login_required
def wallet(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user, amount=0)
    
    return render(request, 'layouts/wallet.html', {'wallet': wallet})
    



from django.core.paginator import Paginator

def filter_products_by_price(request):
    # Initialize the context dictionary
    context = {}

    if request.method == 'POST':
        price_min = Decimal(request.POST.get('price-min', 1000))
        price_max = Decimal(request.POST.get('price-max', 1000000))

        # Query the products within the specified price range
        products = Product.objects.filter(product_price__gte=price_min, product_price__lte=price_max)

    else:
        # If no form is submitted, display all products
        products = Product.objects.all()

    # Pagination
    paginator = Paginator(products, 2)  # Set the number of products per page (e.g., 2 products per page)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    # Add the products and other relevant data to the context dictionary
    context['products'] = products

    # Add any other data you want to pass to the template
    # ...

    return render(request, 'layouts/collections.html', context)


