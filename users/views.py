from django.shortcuts import render,redirect
from admins.models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator




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
    context = {}

    if category is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(product_category__category_name=category)

    # Pagination
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    categories = ProductCategory.objects.all()
    brands = ProductBrand.objects.all()
    context = {
        'products': products,
        'brands': brands,
        'categories': categories,
        'selected_category': category  # Pass the selected category to the template
    }

    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(product_name__icontains=q) | Q(product_description__icontains=q))
        products = products.filter(multiple_q)
        context['products'] = products

    return render(request, 'layouts/collections.html', context)





def product_by_brand(request,id):
    products = Product.objects.filter(product_brand = id)
    categories = ProductCategory.objects.all()
    brands = ProductBrand.objects.all()
    context = {
        'products':products,
        'categories':categories,
        'brands':brands,
    }
    return render(request,'layouts/product_by_brand.html',context)

def product_by_category(request, id):
    products = Product.objects.filter(product_category=id)
    categories = ProductCategory.objects.all()
    brands = ProductBrand.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'layouts/product_by_category.html', context)




def single_product(request, id):
    product = get_object_or_404(Product, id=id)
    context = {
        'product': product
    }
    return render(request, 'layouts/single_product.html', context)


def checkout(request):
    return render(request,'layouts/checkout.html')









