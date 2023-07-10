from django.urls import path
from.import views

urlpatterns = [
    
    path('admin_logout',views.admin_logout,name="admin_logout"),
    path('customers',views.customers,name="customers"),
    path('blockuser/<int:id>',views.block_user,name="blockuser"),
    path('unblockuser/<int:id>',views.unblock_user,name="unblockuser"),
  


    


    path('',views.admin_login,name='admin_login'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('product_list', views.product_list,name='product_list'),
    path('product_add', views.product_add,name='product_add'),
    path('product_edit', views.product_edit,name='product_edit'),
    path('product_update/<str:id>', views.product_update,name='product_update'),
    path('product_delete/<str:id>', views.product_delete,name='product_delete'),
    path('user_home', views.user_home, name='user_home'),
    # path('user_edit/<int:id>', views.user_edit, name='user_edit'),
    # path('user_search', views.user_search, name='user_search'),
    path('block_user/<int:id>', views.block_user, name='block_user'),
    path('unblock_user/<int:id>', views.unblock_user, name='unblock_user'),

    path('category_list', views.category_list,name='category_list'),
    path('category_add', views.category_add,name='category_add'),
    path('category_edit', views.category_edit,name='category_edit'),
    path('category_update/<str:id>',views.category_update,name='category_update'),
    path('category_delete/<str:id>', views.category_delete,name='category_delete'),
    path('change_category_block_status/<str:id>', views.change_category_block_status,name='change_category_block_status'),
    path('brand_list', views.brand_list,name='brand_list'),
    path('brand_add', views.brand_add,name='brand_add'),
    path('brand_edit', views.brand_edit,name='brand_edit'),
    path('brand_update/<str:id>',views.brand_update,name='brand_update'),
    path('brand_delete/<str:id>', views.brand_delete,name='brand_delete'),
    path('change_brand_block_status/<str:id>', views.change_brand_block_status,name='change_brand_block_status'),
    
    path('order_list', views.order_list,name='order_list'),
    # path('order_update/<int:pk>/', views.order_update, name='order_update'),
    path('order_update/<int:id>/', views.order_update, name='order_update'),
    path('coupon', views.coupon,name='coupon'),
    # path('admin_dashboard/coupons/', views.coupon_list, name='coupon_list'),
    path('coupon-add', views.coupon_add, name='coupon_add'),
    path('coupon_edit/<int:coupon_id>/', views.coupon_edit, name='coupon_edit'),
    path('coupon-delete/<int:coupon_id>/', views.coupon_delete, name='coupon_delete'),



   

]