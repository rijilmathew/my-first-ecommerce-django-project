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
from django.db.models.functions import ExtractMonth
from django.db.models import Count,Sum
import calendar
from datetime import date, timedelta
from django.db.models.functions import TruncWeek
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


import datetime



# Create your views here.
@login_required
def admin_home(request):
    orders=Order.objects.annotate(month = ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month','count')
    weekly_orders = Order.objects.annotate(week=TruncWeek('order_date')).values('week').annotate(count=Count('id')).values('week', 'count')
    users = CustomUser.objects.all()
    products = Product.objects.all()


    #todays order
    today = date.today()
    orderss = Order.objects.filter(order_date__date=today)
    order_count = orderss.count()
    #todays order end 


    #total_orders
    total_orders = Order.objects.all()
    total_orders_count =  total_orders.count()
    #total_orders end

    #order_cancel graph
    order_cancel = Order.objects.filter( order_status = 'Cancelled',order_date__date=today)
    no_of_order_cancel =  order_cancel.count()
    #order_cancel end 

    #order cancel report
    cancelled_orders = Order.objects.filter(order_status='Cancelled')
    total_mrp_sum = cancelled_orders.aggregate(total=Sum('total_mrp'))['total']
  
    #order_cancel report end

    # no_of_users
    no_of_users = users.count()
    #no_of_users_end
    #sale report
    sailed_orders = Order.objects.filter(order_status='Delivered')
  




    #sales report end 


    #monthly total sale 
    current_month = now().month
    sales_data = []
    monthlabels = []

    for month in range(1, current_month + 1):
        total_payment_amount = Order.objects.filter(
            order_date__month=month,
            payment_status='Completed'
        ).aggregate(total_payment=Sum('payment_amount'))['total_payment'] or 0

        sales_data.append(float(total_payment_amount))
        month_name = calendar.month_name[month]
        monthlabels.append(month_name)
    
    #monthly total sale end 

    #
    
    monthNumber = []
    totalOrders = []
    productName = []
    productCounts = []
    
    
    
    for product in products:
        productName.append(product.product_name)
        productCount = OrderItem.objects.filter(product=product).count()
        productCounts.append(productCount)
   

    #week days 

    # Get the start and end dates for the desired week
    todday = timezone.now().date()
    current_start_date = today - datetime.timedelta(days=todday.weekday())  # Get the start of the current week (Monday)
    current_end_date = current_start_date +datetime. timedelta(days=6)  # Get the end of the current week (Sunday)

    # Get the start and end dates for the previous week
    previous_start_date = current_start_date -datetime. timedelta(days=7)  # Get the start of the previous week (Monday)
    previous_end_date = previous_start_date + datetime.timedelta(days=6)  # Get the end of the previous week (Sunday)

    # Query data for the current week
    current_week_counts = Order.objects.filter(order_date__range=[current_start_date, current_end_date]).values('order_date__date').annotate(count=Count('id'))
    current_week_dates = [current_start_date +datetime. timedelta(days=day) for day in range(7)]  # Create a list of dates within the current week

    # Create a dictionary to store the count per day for the current week with default 0 value for missing days
    current_counts_per_day = {date: 0 for date in current_week_dates}
    for count in current_week_counts:
        current_counts_per_day[count['order_date__date']] = count['count']

    # Query data for the previous week
    previous_week_counts = Order.objects.filter(order_date__range=[previous_start_date, previous_end_date]).values('order_date__date').annotate(count=Count('id'))
    previous_week_dates = [previous_start_date + timedelta(days=day) for day in range(7)]  # Create a list of dates within the previous week

    # Create a dictionary to store the count per day for the previous week with default 0 value for missing days
    previous_counts_per_day = {date: 0 for date in previous_week_dates}
    for count in previous_week_counts:
        previous_counts_per_day[count['order_date__date']] = count['count']
    

    currentWeekCounts=list(current_counts_per_day.values())
    currentWeekDates= [date.strftime("%A") for date in current_week_dates]
    previousWeekCounts= list(previous_counts_per_day.values())
    previousWeekDates= [date.strftime("%A") for date in previous_week_dates]

    #week days end    

  

    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
       
    
    context = { 'monthNumber':monthNumber,
                'totalOrders':totalOrders,
                'productName':productName,
                'productCounts':productCounts,
                'order_count':order_count,
                'total_orders_count':total_orders_count,
                'no_of_order_cancel':no_of_order_cancel,
                'cancelled_orders': cancelled_orders,
                'total_mrp_sum': total_mrp_sum,
                'no_of_users':no_of_users,
                'sales_data': sales_data,
                'monthlabels': monthlabels,
                'products':products,
                'sailed_orders':sailed_orders,
                'currentWeekCounts':currentWeekCounts,
                'currentWeekDates':currentWeekDates,
                'previousWeekCounts': previousWeekCounts,
                'previousWeekDates':previousWeekDates,
                        

                }       

    
    return render(request,'admins/admin_home.html',context)

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
    user = CustomUser.objects.filter(is_superuser=False)
    return render(request,'admins/user_home.html',{'users':user})

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




#addtocart.............................................................addtocart
def order_list(request):
    orders = Order.objects.all().select_related('user', 'shipping_address').order_by('-order_date')
    paginator = Paginator(orders, 5)  # Create a Paginator object with 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get the current page object

    order_items = OrderItem.objects.all()
    users = get_user_model().objects.all()
    default_addresses = UserAddress.objects.filter(user__in=users, is_default=True)
    products = Product.objects.all()

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
        'page_obj': page_obj,  # Pass the page object to the template
    }
    return render(request, 'admins/oder_list.html', context)



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
#searching   

def order_list_today(request):
    today = date.today()
    orders = Order.objects.filter(order_date__date=today)
    paginator = Paginator(orders, 5)  # Create a Paginator object with 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get the current page object

    order_items = OrderItem.objects.filter(order_no__in=orders)
    users = CustomUser.objects.all()
    products = Product.objects.all()
    product_totals = {}
    for order_item in order_items:
        product_total = order_item.quantity * order_item.product.product_price
        product_totals[order_item.id] = product_total
    
    context = {
               'orders': orders,
               'order_items': order_items, 
               'users': users,
               'product_totals': product_totals, 
               'products': products,
               'page_obj':page_obj, 
            }
    return render(request, 'admins/oder_list.html', context)



def order_list_monthly(request):
    today = date.today()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    orders = Order.objects.filter(
        order_date__range=[start_of_month, end_of_month]
    )
    paginator = Paginator(orders, 5)  # Create a Paginator object with 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get the current page object

    order_items = OrderItem.objects.filter(
       order_no__in=orders
    )
    
    users = CustomUser.objects.all()
    
    products = Product.objects.all()
    product_totals = {}
    for order_item in order_items:
        product_total = order_item.quantity * order_item.product.product_price
        product_totals[order_item.id] = product_total
 
    
    context = {
        'orders': orders,
        'order_items': order_items,
        'users': users,
        'product_totals': product_totals, 
        'products': products,
        'page_obj': page_obj,  # Pass the page object to the template
       
    }
    
    return render(request, 'admins/oder_list.html', context)






def order_list_yearly(request):
    today = date.today()
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)
    
    orders = Order.objects.filter(
        order_date__year=today.year
    )
    paginator = Paginator(orders, 5)  # Create a Paginator object with 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get the current page object

    order_items = OrderItem.objects.filter(
        order_no__in=orders
    )
    
    users = CustomUser.objects.all()
    
    products = Product.objects.all()
    product_totals = {}
    for order_item in order_items:
        product_total = order_item.quantity * order_item.product.product_price
        product_totals[order_item.id] = product_total
    
    
    context = {
        'orders': orders,
        'order_items': order_items,
        'users': users,
        'product_totals': product_totals, 
        'products': products,
        'page_obj':page_obj,
        
    }
    
    return render(request, 'admins/oder_list.html', context)




def order_list_weekly(request):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    orders = Order.objects.filter(
        order_date__range=[start_of_week, end_of_week]
    )
    paginator = Paginator(orders, 5)  # Create a Paginator object with 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get the current page object

    order_items = OrderItem.objects.filter(
         order_no__in=orders
    )
    
    users = CustomUser.objects.all()
    
    products = Product.objects.all()
    product_totals = {}
    for order_item in order_items:
        product_total = order_item.quantity * order_item.product.product_price
        product_totals[order_item.id] = product_total
    
    
    
    context = {
        'orders': orders,
        'order_items': order_items,
        'users': users,
        'product_totals': product_totals, 
        'products': products,
        'page_obj':page_obj,
        
    }
    
    return render(request, 'admins/oder_list.html', context)






def order_list_within_duration(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    users = CustomUser.objects.all()

    products = Product.objects.all()
   
  

    if start_date and end_date:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        print("Formatted Start Date:", start_date)
        print("Formatted End Date:", end_date)

        orders = Order.objects.filter(order_date__range=[start_date, end_date])
        paginator = Paginator(orders, 5)  # Create a Paginator object with 5 orders per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)  # Get the current page object

        order_items = OrderItem.objects.filter(order_no__in=orders)
        product_totals = {}
        for order_item in order_items:
            product_total = order_item.quantity * order_item.product.product_price
            product_totals[order_item.id] = product_total


        print("Filtered Orders:", orders)
        print("Filtered Order Items:", order_items)

        context = {
            'orders': orders,
            'order_items': order_items,
            'users': users,
            'product_totals': product_totals, 
            'products': products,
            'page_obj':page_obj,
            
        }

        return render(request, 'admins/oder_list.html', context)

    return render(request, 'admins/oder_list.html', {'users': users,'products': products,})




# #searching    end



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








