from django.db import models
from admins.models import Product
from authentication.models import CustomUser,UserAddress
from django.contrib.auth import get_user_model
import uuid
from admins.models import Coupon

# Create your models here.



User = get_user_model()
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    

    def sub_total(self):
        return self.product.product_price * self.quantity

    def __str__(self):
        return str(self.product)
    

    
class Order(models.Model):
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Out for Shipping', 'Out for Shipping'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )
    PAYMENT_METHOD = (
        ('COD', 'COD'),
        ('Razorpay', 'Razorpay'),
        ('paid by paypal', 'paid by paypal'),
    )

    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )

    DELIVERY_STATUS = (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )

    order_no = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150,default=None, null=True)
    lname = models.CharField(max_length=150,default=None, null=True)
    email = models.CharField(max_length=150,default=None, null=True)
    phone = models.CharField(max_length=150,default=None, null=True)
    city = models.CharField(max_length=150,default=None, null=True)
    state = models.CharField(max_length=150,default=None, null=True)
    pincode = models.CharField(max_length=150,default=None, null=True)
    address =models.TextField(default=None, null=True)
    payment_id = models.CharField(max_length=250,default=None, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='Pending')
    delivered_status = models.CharField(max_length=50, choices=DELIVERY_STATUS, default=None, null=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS,default='Pending')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD)
    to_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='orders', default=None, null=True)
    total_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2,default=None, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='order_shipments', default=None, null=True)
    

    def __str__(self):
        return f"{self.user.email} - Order No: {str(self.order_no)}"

    def get_total(self):
        order_items = OrderItem.objects.filter(order_no=self)
        total = sum(item.get_subtotal() for item in order_items)
        return total

    def get_total_discount(self):
        if self.coupon:
            return self.get_total() - (self.coupon.discount_price)
        return 0

    def get_total_payment_amount(self):
        if self.coupon:
            return self.get_total() - self.get_total_discount()
        return self.get_total()

class OrderItem(models.Model):
    order_no = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(null=False)

    def __str__(self):
        return str(self.order_no)

    
    def get_subtotal(self):
        return self.quantity * self.product.product_price






class Wishlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Wishlist for {self.user.username}"    
    