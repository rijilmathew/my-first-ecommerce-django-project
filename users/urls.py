from django.urls import path
from.import views
from django.conf import settings
from django.conf.urls.static import static
# from admins.models import Cart


urlpatterns = [
   path('',views.index,name="index"),
   path('product_home',views.product_home,name="product_home"),
   path('product_by_brand',views.product_by_brand,name="product_by_brand"),
   # path('product_by_brand',views.product_by_brand,name="product_by_brand"),
   
   path('single_product/<int:id>/', views.single_product, name='single_product'),
  
  
   

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)