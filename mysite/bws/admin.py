from django.contrib import admin
from .models import Product, Buyer, Seller, BuyerOrder, SellerOrder


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('capacity_calculation',)


class SellerOrderAdmin(admin.ModelAdmin):
    readonly_fields = (
        'buyer_info',
        'buyer_product',
        'get_capacity_calculation',
    )

    def get_capacity_calculation(self, obj):
        if obj.buyer_order and obj.buyer_order.product:
            product = obj.buyer_order.product
            return product.capacity_calculation()
        else:
            return "No Capacity Calculation"

    def buyer_info(self, obj):
        if obj.buyer_order:
            buyer_order = obj.buyer_order
            return buyer_order.buyer.name
        else:
            return 'No Buyer Order'

    def buyer_product(self, obj):
        if obj.buyer_order and obj.buyer_order.buyer:
            return obj.buyer_order.product.name
        else:
            return 'No Buyer Order or Product'

    buyer_product.short_description = 'Product'
    buyer_info.short_description = 'Buyer'
    get_capacity_calculation.short_description = 'Capacity Calculation'


admin.site.register(Product, ProductAdmin)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(BuyerOrder)
admin.site.register(SellerOrder, SellerOrderAdmin)
