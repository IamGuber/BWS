from django.db import models
from django.core.validators import RegexValidator


class Product(models.Model):
    name = models.CharField(verbose_name='Name', max_length=200, unique=True)
    width = models.IntegerField(verbose_name='Width(mm)', default=0)
    length = models.IntegerField(verbose_name='Length(mm)', default=0)
    height = models.IntegerField(verbose_name='Height(mm)', default=0)
    thickness = models.IntegerField(verbose_name='Thickness(mm)', default=0)

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
            last_order = BuyerOrder.objects.order_by('-id').first()
            if last_order:
                last_number = int(last_order.order_nr[3:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.order_nr = f'BWS{new_number:04}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'BuyerOrder'
        verbose_name_plural = 'BuyerOrders'


class SellerOrder(models.Model):
    buyer_order = models.ForeignKey(to='BuyerOrder', on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(to='Seller', on_delete=models.SET_NULL, null=True, blank=True)
    production_product = models.ForeignKey(to='Product', verbose_name='Production Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Quantity', default=0)

    ORDER_STATUS = (
        ('a', 'Accepted'),
        ('p', 'In produce'),
        ('l', 'Loaded'),
        ('y', 'Delivered'),
        ('d', 'Declined'),
    )

    status = models.CharField(verbose_name='Order Status', choices=ORDER_STATUS, default='a', max_length=1, blank=True)

    def __str__(self):
        return str(self.buyer_order)

    class Meta:
        verbose_name = 'SellerOrder'
        verbose_name_plural = 'SellerOrders'
