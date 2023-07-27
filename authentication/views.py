
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
from carts.models import Cart,CartItem,Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from .forms import UserProfileForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import UserAddress
from django.shortcuts import get_object_or_404
from .models import UserProfile
import requests
from decouple import config
import random
from twilio.rest import Client
from django_otp.oath import totp
import string
from django.core.exceptions import ObjectDoesNotExist





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
        if not re.match(r'^[A-Za-z\s]+$', name):
                messages.error(request, "Name must only contain letters and spaces.")
                return redirect('signup')
        # Phone number validation
        if not phone_number.isdigit() or len(phone_number) != 10:
            messages.error(request, "Phone number must contain only 10 digits.")
            return redirect('signup')
        # check the phone_number already exist in data base 
        if CustomUser.objects.filter(phone_number=phone_number).exists():
              messages.error(request, "Phone number already exists. Please use a different phone number or log in using the existing account.")
              return redirect('signup') 
           
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email.")
            return redirect('signup')
        # Generate OTP
        import random
        otp = ''.join(random.choices('0123456789', k=6))
        
        # Save user data in session
        request.session['signup_data'] = {
            'email': email,
            'password': password,
            'name': name,
            'phone_number': phone_number,
            'otp': otp
        }

        # Send OTP email
        send_mail(
            'Email Verification',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        
        return redirect('verify_otp')
    
    return render(request, 'authentication/signup.html')


def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        
        try:
            # Retrieve user data from session
            signup_data = request.session.get('signup_data')
            if not signup_data:
                return redirect('verify_otp')
            
            # Validate OTP
            if otp != signup_data['otp']:
                error_message = 'Invalid OTP. Please try again.'
                return render(request, 'authentication/verify_otp.html', {'error_message': error_message})
            
            # Clear the session data
            request.session.pop('signup_data')
            
            # Create user and save it to the database only after OTP verification
            user = CustomUser.objects.create_user(
                email=signup_data['email'],
                password=signup_data['password'],
                name=signup_data['name'],
                phone_number=signup_data['phone_number'],
                otp=signup_data['otp'],
                is_active=True
            )
            
            # Redirect to user login or any other desired page
            return redirect('user_login')
        except CustomUser.DoesNotExist:
            return redirect('verify_otp')
    
    return render(request, 'authentication/verify_otp.html')

    
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user =authenticate(request, email=email, password=password)
        if user is not None and not user.is_staff:
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
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=')for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                    
            except:
                   return redirect('/') 
            
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('user_login')
    
    return render(request, 'authentication/login.html')

#mobile Otp
class OtpGenerate():
    Otp=None
    phone=None

    def send_otp(phone):
        account_sid=config('account_sid')
        auth_token=config('auth_token')
        target_number = '+919447595446' 
        twilio_number=config('twilio_number')
        otp=random.randint(1000,9999)
        OtpGenerate.Otp=str(otp)
        OtpGenerate.phone=phone
        msg="your otp is " + str(otp)
        client=Client(account_sid,auth_token)
        message=client.messages.create(
            body=msg,
            from_=twilio_number,
            to=target_number
        )
        print(message.body)
        return True


def otp_login(request):
    
    return render(request, 'authentication/otplogin.html')

def login_otp(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'GET' and request.GET.get('phone_number'):
        phone_number = request.GET.get('phone_number')
        
        try:
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                OtpGenerate.send_otp(phone_number)
                return redirect('otp')
            else:
                 messages.error(request, 'Phone Number is not registered')
                 return redirect('otp_login')
        except ObjectDoesNotExist:
            messages.error(request, 'Phone Number is not registered')
            return redirect('otp_login')
            
    else:
        messages.error(request, 'Please provide your phone number')
        return redirect('otp_login')



def otp(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request,'authentication/otp.html')


def verify_mobileotp(request):
    obj = OtpGenerate()
    if request.method == 'POST':
        re_otp = request.POST.get('otp')
        ge_otp = obj.Otp
        if re_otp == ge_otp:
            user = CustomUser.objects.get(phone_number=obj.phone)
            if user.is_active == True:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user = user
                            item.save()
                except Cart.DoesNotExist:
                    pass
                login(request, user)
                return redirect('/')  # Redirect to the desired page after successful verification
            else:
                messages.error(request, "Invalid Credentials")
                return redirect('otp')
        else:
            messages.error(request, "Invalid OTP")
            return redirect('otp')
    else:
        messages.error(request, "Invalid Request")
        return redirect('otp')
#mobile otp end 

def user_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/')

@login_required(login_url='user_login')
def profile(request):
    user = request.user
    addresses = Order.objects.filter(user=request.user).values(
            'fname', 'lname', 'email', 'phone', 'address', 'city', 'state', 'pincode'
        ).distinct()
    context  = {
        'user':user,
        'addresses':addresses,
    }

    return render(request, 'authentication/profile.html',context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        user = request.user
        user.name = name
        user.email = email
        user.phone_number = phone_number
        user.save()

        messages.success(request, 'Profile information updated successfully.')
        return redirect('profile')

    return redirect('profile')  



@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        user = authenticate(request, email=request.user.email, password=current_password)
        if user is not None:
            if new_password == confirm_new_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Your password has been changed successfully.')
            else:
                messages.error(request, 'New password and confirm password do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')

        return redirect('profile')

    return render(request, 'authentication/profile.html')

#forgot Password 

def forgot_password(request):
    return render( request, 'authentication/forgot_password.html')

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            # Generate OTP
            otp = ''.join(random.choices(string.digits, k=6))
            user.otp = otp
            user.save()

            # Send OTP via email
            send_mail(
                'Email Verification',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            # Redirect to OTP verification page
            return redirect(verify_forgot_otp,email=email)
        else:
            messages.error(request,'Email not found please check the email address or register a new account')
            return redirect('forgot_password')
    
    return render(request, 'authentication/forgot_password.html')



def verify_forgot_otp(request,email=None):  # Add the email parameter here
    if request.method == 'POST':
        email = request.POST.get('email')
        user_otp = request.POST.get('otp')

        user = CustomUser.objects.filter(email=email,otp=user_otp).first()
       


        if user:
            # Reset the OTP after successful verification
            user.otp = None
            user.save()

            # Redirect to the page for adding a new password
            return redirect('add_new_password')
        else:
            # Handle the case when the entered OTP is invalid
            # Redirect back to the same OTP verification page with the email as a parameter
            return redirect('verify_forgot_otp',)  # Redirect to the same page with the email as a parameter
    else:
        # If the request is GET, display the OTP verification page with the email if available
        return render(request, 'authentication/otp_verification.html', {'email': email})
    


def add_new_password(request,email=None):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        new_password = request.POST.get('new_password')


        user = CustomUser.objects.filter(email=email).first()
        password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$'
        if not re.match(password_pattern, new_password):
            messages.error(request, "Password must contain at least one uppercase letter, one digit, one special character, and be at least 6 characters long.")
            return redirect('add_new_password')
    

        if user:
            # Set the new password for the user
            user.set_password(new_password)
            user.save()

            # Redirect to the login page or any other page as needed
            return redirect('user_login')  # Replace 'login' with the appropriate URL name for your login page
        else:
            # Handle the case when the user email is not found
            messages.error(request, 'User not found.')
            return redirect('verify_forgot_otp')  # Redirect back to the OTP verification page

    return render(request, 'authentication/add_new_password.html',{'email': email})





