from django.contrib import admin
from .models import Product, Buyer, Seller, BuyerOrder, SellerOrder
from .forms import SellerOrderForm


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('capacity_calculation',)


class SellerOrderAdmin(admin.ModelAdmin):
    form = SellerOrderForm
    readonly_fields = ('get_capacity_calculation',)

    def get_capacity_calculation(self, obj):
        if obj.buyer_order and obj.buyer_order.product:
            product = obj.buyer_order.product
            return product.capacity_calculation()
        else:
            return "No Capcity Calculation"

    get_capacity_calculation.short_description = 'Capacity Calculation'


admin.site.register(Product, ProductAdmin)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(BuyerOrder)
admin.site.register(SellerOrder, SellerOrderAdmin)
