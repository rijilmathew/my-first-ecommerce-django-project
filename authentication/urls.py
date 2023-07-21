from django.urls import path
from.import views

urlpatterns = [
path('user_login',views.user_login,name="user_login"),
path('signup',views.signup,name="signup"),
path('verify-otp',views.verify_otp, name='verify_otp'),
path('logout',views.user_logout,name="logout"),
path('profile', views.profile, name='profile'),
path('change-password', views.change_password, name='change_password'),
path('update_profile', views.update_profile, name='update_profile'),


path('otp-login',views.otp_login,name="otp_login"),
path('login-otp',views.login_otp,name="login_otp"),
path('otp',views.otp,name="otp"),
path('verify_mobileotp',views.verify_mobileotp,name="verify_mobileotp"),

path('forgot_password',views.forgot_password,name="forgot_password"),
path('send_otp',views.send_otp,name="send_otp"),
path('verify_forgot_otp',views.verify_forgot_otp,name="verify_forgot_otp"),
path('forgot_otp/<str:email>/',views.verify_forgot_otp,name="verify_forgot_otp"),
path('add_new_password',views.add_new_password,name="add_new_password"),



  
  

]