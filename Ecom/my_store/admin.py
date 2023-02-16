from .models import *
from django.contrib import admin

admin.site.register(Customer)
admin.site.register(Product)


# def ship_order(modeladmin, request, queryset):
#     queryset.update(status='s')
# ship_order.short_description = 'Mark Selected Orders as Shipped'

# class OrderAdmin(admin.ModelAdmin):
#     actions = [ship_order]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order',)
    
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'address', 'city', 'state', 'zipcode')
    list_filter = ('order', 'customer')

admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)