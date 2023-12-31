from django.contrib import admin
from .models import Cart,CartItem,Order,OrderItem,Wishlist,Wallet

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')
    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active')

admin.site.register(Cart)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(Wallet)