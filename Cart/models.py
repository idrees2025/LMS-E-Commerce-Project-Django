from django.db import models
from django.conf import settings
from django.utils import timezone
from Shop.models import Product
# Create your models here.
STATUS_CHOICES = (
        ('pending','pending'),
        ('on the way','on the way'),
        ('failed','failed'),
        ('refund','refund'),
        ('shipped','shipped'),
        ('delivered','delivered'),
        ('cancelled','cancelled'),
    )

class CartItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def total_price(self):
        return float(self.product.discounted_price()*self.quantity)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.price * self.quantity

class ShippingAddress(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=222)
    last_name=models.CharField(max_length=222)
    company_name=models.CharField(max_length=222,blank=True,null=True)
    area_code=models.CharField(max_length=22)
    phone_number=models.CharField(max_length=222)
    street_address=models.CharField(max_length=222)
    zip_code=models.CharField(max_length=22)
    is_buisness=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
