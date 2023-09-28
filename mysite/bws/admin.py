from django.contrib import admin
from .models import Product, Buyer, Seller, BuyerOrder, SellerOrder, Trailer


class BuyerOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_nr',
        'buyer',
        'product',
    )


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('capacity_calculation',)


class SellerOrderAdmin(admin.ModelAdmin):
    list_display = (
        'buyer_order',
        'seller',
        'production_product',
    )
    readonly_fields = (
        'capacity_calculation',
        'buyer_info',
        'buyer_product',
        'get_capacity_calculation',
        'get_buyer_price',
        'price_calculation',
    )

    def price_calculation(self, obj):
        return obj.price_calculation()

    def capacity_calculation(self, obj):
        return obj.capacity_calculation()

    def get_buyer_price(self, obj):
        if obj.buyer_order:
            return obj.buyer_order.buyer_price
        else:
            return None

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

    price_calculation.short_description = 'Profit'
    capacity_calculation.short_description = 'Modified Capacity Calculation'
    buyer_product.short_description = 'Product'
    buyer_info.short_description = 'Buyer'
    get_capacity_calculation.short_description = 'Capacity Calculation from Buyer Order'
    get_buyer_price.short_description = 'Buyer Price'

    fieldsets = (
        (None, {
            'fields': (
                'buyer_order',
                'seller',
                'production_product',
                'trailer',
                'seller_price',
                'transport_price',
                'quantity',
                'price_calculation',
                'total_price',
                'capacity_calculation',
                'buyer_info',
                'buyer_product',
                'get_capacity_calculation',
                'get_buyer_price',
            ),
        }),
        ('Status', {
            'fields': (
                'status',
            ),
        }),
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(BuyerOrder, BuyerOrderAdmin)
admin.site.register(SellerOrder, SellerOrderAdmin)
admin.site.register(Trailer)
