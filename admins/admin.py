from django.contrib import admin
from .models import *

# Register your models here.
  
admin.site.register(ProductBrand)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Filter_Price)
admin.site.register(Coupon)

