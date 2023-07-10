from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),

    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout',views.checkout,name='checkout'),
    path('place-order',views.placeorder,name='placeorder'),

    path('order_summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('order_history',views.order_history,name='order_history'),
    path('wishlist/',views.wishlist_view, name='wishlist'),
    path('add_to_wishlist/',views.add_to_wishlist, name='add_to_wishlist'),
    path('order-view/<str:od_no>',views.vieworder,name='vieworder'),
]