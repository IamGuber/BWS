from django.contrib import admin
from .models import Product, Buyer, Seller, BuyerOrder, SellerOrder, Trailer, Order, Transport, TransportCompany
from .forms import BuyerOrderForm, SellerOrderForm


class TransportAdmin(admin.ModelAdmin):
    list_display = (
        'seller_order',
        'transport_company',
        'truck_plates',
        'status',
        'mail',
    )

    readonly_fields = (
        'display_seller_info',
        'display_buyer_info',
        'get_buyer_product',
        'get_buyer_info',
        'get_buyer_date',
        'get_seller_info',
        'get_production_product',
        'get_trailer',
        'get_transport_price',
        'get_quantity',
        'get_production_date',
    )

    fieldsets = (
        (None, {
            'fields': (
                'seller_order',
                'transport_company',
                'trailer',
                'truck_plates',
                'loading_date',
                'unloading_date',
                'info',
            )
        }),
        ('Production and Loading Information', {
            'fields': (
                'display_seller_info',
                'get_seller_info',
                'get_production_product',
                'get_trailer',
                'get_transport_price',
                'get_quantity',
                'get_production_date',
            )
        }),
        ('Customer Information', {
            'fields': (
                'display_buyer_info',
                'get_buyer_info',
                'get_buyer_product',
                'get_buyer_date',
            )
        }),
        ('Status', {
            'fields': (
                'status',
            ),
        }),
        ('Mail Send Status', {
            'fields': (
                'mail',
            ),
        }),
    )

    def get_production_date(self, obj):
        if obj.seller_order:
            return obj.seller_order.production_date
        return 'No Production Date'

    def get_quantity(self, obj):
        if obj.seller_order:
            return obj.seller_order.quantity
        return 'No Quantity Info'

    def get_transport_price(self, obj):
        if obj.seller_order:
            return obj.seller_order.transport_price
        return 'No Transport Price'

    def get_trailer(self, obj):
        if obj.seller_order:
            return obj.seller_order.trailer
        return 'No Trailer Info'

    def get_production_product(self, obj):
        if obj.seller_order:
            return obj.seller_order.production_product
        return 'No Production Product'

    def get_seller_info(self, obj):
        if obj.seller_order:
            return obj.seller_order.seller.info
        return 'No Seller Info'

    def display_seller_info(self, obj):
        if obj.seller_order:
            return obj.seller_order.seller
        return 'No Seller Order'

    def get_week_numbers(self, start_date, end_date):
        start_week_number = start_date.strftime('%W')
        end_week_number = end_date.strftime('%W')
        return f'Week {start_week_number} - Week {end_week_number}'

    def get_buyer_date(self, obj):
        if obj.seller_order.buyer_order and obj.seller_order.buyer_order.delivery_date_from and obj.seller_order.buyer_order.delivery_date_to:
            start_date = obj.seller_order.buyer_order.delivery_date_from
            end_date = obj.seller_order.buyer_order.delivery_date_to
            return self.get_week_numbers(start_date, end_date)
        else:
            return 'No Delivery Date'

    def get_buyer_product(self, obj):
        if obj.seller_order:
            return obj.seller_order.buyer_order.product
        else:
            return 'No Buyer Product'

    def get_buyer_info(self, obj):
        if obj.seller_order:
            return obj.seller_order.buyer_order.buyer.info
        else:
            return 'No Buyer Information'

    def display_buyer_info(self, obj):
        if obj.seller_order:
            return obj.seller_order.buyer_order.buyer.name
        else:
            return 'No Buyer Information'

    display_buyer_info.short_description = 'Buyer'
    get_buyer_info.short_description = 'Buyer Information'
    get_buyer_product.short_description = 'Buyer Ordered Product'
    get_buyer_date.short_description = 'Buyer Preferred Delivery Date'
    display_seller_info.short_description = 'Seller'
    get_seller_info.short_description = 'Seller Information'
    get_production_product.short_description = 'Product for Loading'
    get_trailer.short_description = 'Trailer'
    get_transport_price.short_description = 'Counted Transport Price'
    get_quantity.short_description = 'Loading Quantity'
    get_production_date.short_description = 'Ready for Loading'


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
        'get_transport_company',
        'get_truck_plates',
        'get_transport_load_date',
        'get_transport_unload_date',
        'get_product',
    )

    fieldsets = (
        ('Common Information', {
            'fields': (
                'order_nr',
                'creating_date',
                'get_product',
                'price',
                'order_status',
            )
        }),
        ('Buyer Information', {
            'fields': (
                'display_buyer_info',
                'get_buyer_date',
            )
        }),
        ('Seller Information', {
            'fields': (
                'display_seller_info',
                'production_date',
            )
        }),
        ('Transport Information', {
            'fields': (
                'get_transport_company',
                'get_truck_plates',
                'get_transport_load_date',
                'get_transport_unload_date',
            )
        }),
        ('Download File', {
            'fields': (
                'export_format',
            ),
        }),
    )

    def get_product(self, obj):
        if obj.buyer_info:
            return obj.buyer_info.product

    def get_transport_unload_date(self, obj):
        if obj.transport_unload_date:
            return obj.transport_load_date.unloading_date.strftime('%Y-%m-%d')

    def get_transport_load_date(self, obj):
        if obj.transport_load_date:
            return obj.transport_load_date.loading_date.strftime('%Y-%m-%d')

    def get_truck_plates(self, obj):
        return obj.transport_plates.truck_plates

    def get_transport_company(self, obj):
        if obj.transport:
            return obj.transport
        return 'No Transport Company'

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

    get_product.short_description = 'Ordered Product'
    get_buyer_date.short_description = 'Preferred delivery date '
    display_buyer_info.short_description = 'Buyer'
    display_seller_info.short_description = 'Seller'


class BuyerOrderAdmin(admin.ModelAdmin):
    form = BuyerOrderForm

    list_display = (
        'order_nr',
        'buyer',
        'product',
        'mail',
    )

    fieldsets = (
        (None, {
            'fields': (
                'order_nr',
                'buyer',
                'product',
                'buyer_price',
                'delivery_date_from',
                'delivery_date_to',
            )
        }),
        ('Status', {
            'fields': (
                'status',
            ),
        }),
        ('Mail Send Status', {
            'fields': (
                'mail',
            ),
        }),
    )


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('capacity_calculation',)


class SellerOrderAdmin(admin.ModelAdmin):
    form = SellerOrderForm

    list_display = (
        'buyer_order',
        'seller',
        'production_product',
        'mail',
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

    fieldsets = (
        ('Common Information', {
            'fields': (
                'buyer_order',
                'seller',
                'production_product',
                'trailer',
            ),
        }),
        ('Counting', {
            'fields': (
                'seller_price',
                'transport_price',
                'quantity',
                'total_price',
            ),
        }),
        ('Counting Result', {
            'fields': (
                'price_calculation',
                'capacity_calculation',
            ),
        }),
        ('Date of Manufacture', {
            'fields': (
                'production_date',
            ),
        }),
        ('Customer Information', {
            'fields': (
                'buyer_info',
                'buyer_product',
                'get_capacity_calculation',
                'get_buyer_price',
                'get_buyer_date',
            ),
        }),
        ('Status', {
            'fields': (
                'status',
            ),
        }),
        ('Mail Send Status', {
            'fields': (
                'mail',
            ),
        }),
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


admin.site.register(Product, ProductAdmin)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(BuyerOrder, BuyerOrderAdmin)
admin.site.register(SellerOrder, SellerOrderAdmin)
admin.site.register(Trailer)
admin.site.register(Order, OrderAdmin)
admin.site.register(Transport, TransportAdmin)
admin.site.register(TransportCompany)
