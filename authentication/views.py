from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from django.utils import timezone,datetime_safe
from django.contrib import messages
import re
from carts.views import _cart_id 
from carts.models import Cart,CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserProfileForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserAddressForm
from .models import UserAddress
from django.shortcuts import get_object_or_404
from .models import UserProfile


# Create your views here.
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')

          # Password validation
        password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$'
        if not re.match(password_pattern, password):
            messages.error(request, "Password must contain at least one uppercase letter, one digit, one special character, and be at least 6 characters long.")
            return redirect('signup')
        
         # Name validation
        if not re.match(r'^[a-zA-Z]+$', name):
            messages.error(request, "Name must only contain letters.")
            return redirect('signup')
        
        # Phone number validation
        if not phone_number.isdigit() or len(phone_number) != 10:
            messages.error(request, "Phone number must contain only 10 digits.")
            return redirect('signup')

      
        # Generate OTP
        import random
        otp = ''.join(random.choices('0123456789', k=6))
        
        # Create user
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            name=name,
            phone_number=phone_number,
            otp=otp,
            is_active=False
        )
        
        # Send OTP email
        send_mail(
            'Email Verification',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        request.session['otp_created_at'] = timezone.now().isoformat()
        return redirect('verify_otp')
    
    return render(request, 'authentication/signup.html')


def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        
        try:
            user = CustomUser.objects.get(email=email, otp=otp)
            otp_created_at_str = request.session.get('otp_created_at')

            if otp_created_at_str is None:
                return redirect('verify_otp')
            otp_created_at = datetime_safe.datetime.fromisoformat(otp_created_at_str)
            current_time = timezone.now()
            if (current_time - otp_created_at).total_seconds() > 300:
                error_message = 'OTP has expired. Please request a new OTP.'
                return render(request, 'authentication/verify_otp.html', {'error_message': error_message})
            user.is_active = True
            user.save()

            customers = CustomUser.objects.all()


            request.session.pop('otp_created_at')
            return redirect('user_login')
        except CustomUser.DoesNotExist:
            return redirect('verify_otp')
    
    return render(request, 'authentication/verify_otp.html')
    
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user =authenticate(request, email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user=user
                        item.save()
            except Cart.DoesNotExist:
                pass            
            login(request, user)
            return redirect('/') 
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('user_login')
    
    return render(request, 'authentication/login.html')
def user_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/')

@login_required
def profile(request):
    user = request.user
    return render(request, 'authentication/profile.html', {'user': user})

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'authentication/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    user = request.user

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user)
    
    return render(request, 'authentication/change_password.html', {'form': form})

#..................................#adress.......................................
@login_required
def show_addresses(request):
    addresses = UserAddress.objects.filter(user=request.user)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        return render(request, 'authentication/show_addresses.html', {'addresses': addresses, 'user_profile': user_profile})
    except UserProfile.DoesNotExist:
        print('user none')
        # Handle the case where UserProfile does not exist for the user
        return render(request, 'authentication/show_addresses.html', {'addresses': addresses, 'user_profile': None})


@login_required
def add_address(request):
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully.')
            return redirect('show_addresses')
    else:
        form = UserAddressForm()
    return render(request, 'authentication/add_address.html', {'form': form})

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    if request.method == 'POST':
        form = UserAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully.')
            return redirect('show_addresses')
    else:
        form = UserAddressForm(instance=address)
    return render(request, 'authentication/edit_address.html', {'form': form, 'address': address})


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('show_addresses')

@login_required
def choose_default_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    request.user.default_address = address
    request.user.save()
    messages.success(request, 'Default address updated successfully.')
    return redirect('show_addresses')


