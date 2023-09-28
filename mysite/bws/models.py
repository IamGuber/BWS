from django.db import models
from django.core.validators import RegexValidator


class Trailer(models.Model):
    name = models.CharField(verbose_name='Trailer Name', max_length=200)
    height = models.IntegerField(verbose_name='Height', default=0)
    width = models.IntegerField(verbose_name='Width', default=0)
    length = models.IntegerField(verbose_name='Length', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Trailer'
        verbose_name_plural = 'Trailers'


class Product(models.Model):
    name = models.CharField(verbose_name='Name', max_length=200, unique=True)
    width = models.IntegerField(verbose_name='Width(mm)', default=0)
    length = models.IntegerField(verbose_name='Length(mm)', default=0)
    height = models.IntegerField(verbose_name='Height(mm)', default=0)
    thickness = models.IntegerField(verbose_name='Thickness(mm)', default=0)
    trailer = models.ForeignKey(to=Trailer, verbose_name='Trailer', on_delete=models.SET_NULL, null=True, blank=True)

    def capacity_calculation(self):
        trailer_height = self.trailer.height
        trailer_width = self.trailer.width
        trailer_length = self.trailer.length
        if self.width and self.length and self.height and self.thickness != 0:
            calculate_height = int(trailer_height / (self.height + (self.thickness * 2)))
            calculate_width = int(trailer_width / (self.width + (self.thickness * 2)))
            calculate_length = int(trailer_length / (self.length + (self.thickness * 2)))
            general_calculate = int(calculate_length * calculate_height * calculate_width)
        else:
            general_calculate = 0

        return general_calculate

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Buyer(models.Model):
    name = models.CharField(verbose_name='Name', max_length=1000)
    email = models.EmailField(verbose_name='Email')
    tel_number = models.CharField(
        verbose_name="Telephone Number",
        max_length=15,
        validators=[RegexValidator(regex=r'^\+370\d{8}$',
                                   message="Lithuanian phone number must start with +370 and have 8 additional digits.",
                                   code='invalid_phone_number'
                                   )
                    ]
    )
    info = models.TextField(verbose_name='Additional Information', max_length=5000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Buyer'
        verbose_name_plural = 'Buyers'


class Seller(models.Model):
    name = models.CharField(verbose_name='Name', max_length=1000)
    email = models.EmailField(verbose_name='Email')
    tel_number = models.CharField(
        verbose_name="Telephone Number",
        max_length=15,
        validators=[RegexValidator(regex=r'^\+370\d{8}$',
                                   message="Lithuanian phone number must start with +370 and have 8 additional digits.",
                                   code='invalid_phone_number'
                                   )
                    ]
    )
    info = models.TextField(verbose_name='Additional Information', max_length=5000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'


class BuyerOrder(models.Model):
    order_nr = models.CharField(max_length=10, unique=True, blank=True)
    buyer = models.ForeignKey(to='Buyer', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(to='Product', on_delete=models.SET_NULL, null=True, blank=True)
    buyer_price = models.DecimalField(verbose_name='Buyer Price', max_digits=10, decimal_places=2, default=0.0)

    ORDER_STATUS = (
        ('a', 'Accepted'),
        ('p', 'In produce'),
        ('l', 'Loaded'),
        ('y', 'Delivered'),
        ('d', 'Declined'),
    )

    status = models.CharField(verbose_name='Order Status', choices=ORDER_STATUS, default='a', max_length=1, blank=True)

    def __str__(self):
        return self.order_nr

    def save(self, *args, **kwargs):
        if not self.order_nr:
            used_order_numbers = BuyerOrder.objects.values_list('order_nr', flat=True)
            new_number = 1
            while f'BWS{new_number:04}' in used_order_numbers:
                new_number += 1
            self.order_nr = f'BWS{new_number:04}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'BuyerOrder'
        verbose_name_plural = 'BuyerOrders'


class SellerOrder(models.Model):
    buyer_order = models.ForeignKey(to='BuyerOrder', on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(to='Seller', on_delete=models.SET_NULL, null=True, blank=True)
    production_product = models.ForeignKey(to='Product', verbose_name='Production Product', on_delete=models.SET_NULL, null=True, blank=True)
    trailer = models.ForeignKey(to=Trailer, verbose_name='Trailer', on_delete=models.SET_NULL, null=True, blank=True)
    seller_price = models.DecimalField(verbose_name='Seller Price', max_digits=10, decimal_places=2, default=0.0)
    transport_price = models.DecimalField(verbose_name='Transport Price', max_digits=10, decimal_places=2, default=0.0)
    quantity = models.IntegerField(verbose_name='Quantity', default=0)
    total_price = models.DecimalField(verbose_name='Total Price', max_digits=10, decimal_places=2, default=0.0)

    ORDER_STATUS = (
        ('a', 'Accepted'),
        ('p', 'In produce'),
    )

    status = models.CharField(verbose_name='Order Status', choices=ORDER_STATUS, default='a', max_length=1, blank=True)

    def price_calculation(self):
        price_from_seller = self.seller_price * self.quantity
        total_price = self.total_price * self.quantity
        profit = (total_price - price_from_seller) - self.transport_price
        return profit

    def capacity_calculation(self):
        trailer_height = self.trailer.height
        trailer_width = self.trailer.width
        trailer_length = self.trailer.length
        if self.production_product and self.production_product.length and self.production_product.height and self.production_product.thickness != 0:
            calculate_height = int(trailer_height / (self.production_product.height + (self.production_product.thickness * 2)))
            calculate_width = int(trailer_width / (self.production_product.width + (self.production_product.thickness * 2)))
            calculate_length = int(trailer_length / (self.production_product.length + (self.production_product.thickness * 2)))
            general_calculate = int(calculate_length * calculate_height * calculate_width)
        else:
            general_calculate = 0

        return general_calculate

    def __str__(self):
        return str(self.buyer_order)

    class Meta:
        verbose_name = 'SellerOrder'
        verbose_name_plural = 'SellerOrders'


class Order(models.Model):
    ...
