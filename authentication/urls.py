from django.urls import path
from.import views

urlpatterns = [
path('user_login',views.user_login,name="user_login"),
path('signup',views.signup,name="signup"),
path('verify-otp',views.verify_otp, name='verify_otp'),
path('logout',views.user_logout,name="logout"),
path('profile', views.profile, name='profile'),
path('change-password', views.change_password, name='change_password'),
path('edit-profile', views.edit_profile, name='edit_profile'),
path('show_addresses', views.show_addresses, name='show_addresses'),
path('add_address', views.add_address, name='add_address'),
path('addresses/<int:address_id>/edit/', views.edit_address, name='edit_address'),
path('addresses/<int:address_id>/delete/', views.delete_address, name='delete_address'),
path('addresses/<int:address_id>/select/', views.choose_default_address, name='choose_default_address'),

]