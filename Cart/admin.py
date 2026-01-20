from django.contrib import admin
from Cart.models import ShippingAddress,Order,OrderItem,CartItem
# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)