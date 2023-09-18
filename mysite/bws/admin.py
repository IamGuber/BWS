from django.contrib import admin
from .models import Product, Buyer, Seller, BuyerOrder, SellerOrder
from .forms import SellerOrderForm


class SellerOrderAdmin(admin.ModelAdmin):
    form = SellerOrderForm


admin.site.register(Product)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(BuyerOrder)
admin.site.register(SellerOrder, SellerOrderAdmin)
