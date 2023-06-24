from django.urls import path
from.import views

urlpatterns = [
path('user_login',views.user_login,name="user_login"),
path('signup',views.signup,name="signup"),
path('verify-otp',views.verify_otp, name='verify_otp'),
path('logout',views.user_logout,name="logout"),
]