from .models import *
from django.contrib import admin

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)



class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order',)
    
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'address', 'city', 'state', 'zipcode')
    list_filter = ('order', 'customer')

admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)