from django.urls import path
from.import views
from django.conf import settings
from django.conf.urls.static import static
# from admins.models import Cart


urlpatterns = [
   path('',views.index,name="index"),
   path('product_home',views.product_home,name="product_home"),
   
   path('single_product/<int:id>/', views.single_product, name="single_product"),
   
   path('search',views.search,name="search"),
   path('wallet',views.wallet,name="wallet"),
   path('filter_products_by_price',views.filter_products_by_price,name="filter_products_by_price"),
  
  
  
   

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)