from django.db import models
from django.urls import reverse
from authentication.models import CustomUser
from django.utils import timezone
from django.utils.text import slugify




class ProductBrand(models.Model):
   brand_name = models.CharField(max_length=50,unique=True)
   
   def __str__(self):
      return self.brand_name


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    
    def get_url(self):
        return reverse('product_by_category', args=[self.id])

    def __str__(self):
        return self.category_name
   




class Product(models.Model):
   product_name = models.CharField(max_length=100,unique=True) 
   product_category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,default=True,null=False)
   product_brand = models.ForeignKey(ProductBrand,on_delete=models.CASCADE)
#    product_price = models.IntegerField() 
   product_price = models.DecimalField(max_digits=10, decimal_places=2)
   product_description = models.TextField(max_length=500,blank=True)
   product_thumbnail = models.ImageField(upload_to='images/products',default=None,blank=True,null=True)
   new_arrival = models.BooleanField(default=False)
   best_product = models.BooleanField(default=False)
   product_quantity = models.IntegerField(null=False,blank=False,default=0)
   created_at = models.DateTimeField(default=timezone.now)
   slug = models.SlugField(unique=True, max_length=100, blank=True)



   def __str__(self):
      return self.product_name
   def get_url(self):
      return reverse('product_description',args=[self.product_category])
   
   def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
   
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image1= models.ImageField(upload_to='images/products',null=True, blank=True)
    image2= models.ImageField(upload_to='images/products',null=True, blank=True)
    image3= models.ImageField(upload_to='images/products',null=True, blank=True)

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)