from django.contrib import admin
from .models import Product, Buyer, Seller, BuyerOrder, SellerOrder, Trailer, Order, Transport, TransportCompany


class TransportAdmin(admin.ModelAdmin):
    list_display = (
        'buyer_order',
        'transport_company',
        'truck_plates',
    )

    readonly_fields = (

    )

    fieldsets = (
        (None, {
            'fields': (
                'buyer_order',
                'transport_company',
                'trailer',
                'truck_plates',
            )
        }),
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_nr',
        'order_status',
    )
    readonly_fields = (
        'order_nr',
        'creating_date',
        'display_buyer_info',
        'display_seller_info',
        'order_status',
        'price',
        'production_date',
        'get_buyer_date',
    )

    fieldsets = (
        (None, {
            'fields': (
                'order_nr',
                'creating_date',
                'display_buyer_info',
                'get_buyer_date',
                'display_seller_info',
                'price',
                'production_date',
                'order_status',
            )
        }),
    )

    def get_week_numbers(self, start_date, end_date):
        start_week_number = start_date.strftime('%W')
        end_week_number = end_date.strftime('%W')
        return f'Week {start_week_number} - Week {end_week_number}'

    def get_buyer_date(self, obj):
        if obj.buyer_info and obj.buyer_info.delivery_date_from and obj.buyer_info.delivery_date_to:
            start_date = obj.buyer_info.delivery_date_from
            end_date = obj.buyer_info.delivery_date_to
            return self.get_week_numbers(start_date, end_date)
        else:
            return 'No Delivery Date'

    def display_seller_info(self, obj):
        if obj.seller_info:
            buyer_order = obj.seller_info
            return buyer_order.seller.name
        else:
            return 'No Seller Order'

    def display_buyer_info(self, obj):
        if obj.buyer_info:
            buyer_order = obj.buyer_info
            return buyer_order.buyer.name
        else:
            return 'No Buyer Order'

    get_buyer_date.short_description = 'Preferred delivery date '
    display_buyer_info.short_description = 'Buyer'
    display_seller_info.short_description = 'Seller'


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
        'get_buyer_date',
    )

    def get_week_numbers(self, start_date, end_date):
        start_week_number = start_date.strftime('%W')
        end_week_number = end_date.strftime('%W')
        return f'Week {start_week_number} - Week {end_week_number}'

    def get_buyer_date(self, obj):
        if obj.buyer_order and obj.buyer_order.delivery_date_from and obj.buyer_order.delivery_date_to:
            start_date = obj.buyer_order.delivery_date_from
            end_date = obj.buyer_order.delivery_date_to
            return self.get_week_numbers(start_date, end_date)
        else:
            return 'No Delivery Date'

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
            return f'No Buyer Order'

    def buyer_product(self, obj):
        if obj.buyer_order and obj.buyer_order.buyer:
            return obj.buyer_order.product.name
        else:
            return 'No Buyer Order or Product'

    get_buyer_date.short_description = 'Delivery Date'
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
                'get_buyer_date',
                'production_date',
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
admin.site.register(Order, OrderAdmin)
admin.site.register(Transport, TransportAdmin)
admin.site.register(TransportCompany)
