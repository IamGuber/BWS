from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db.models import signals
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group


class Transport(models.Model):
    seller_order = models.OneToOneField(to='SellerOrder', on_delete=models.SET_NULL, null=True, blank=True)
    transport_company = models.ForeignKey(to='TransportCompany', verbose_name='Transport Company', on_delete=models.CASCADE, null=True, blank=True)
    trailer = models.ForeignKey(to='Trailer', verbose_name='Trailer', on_delete=models.SET_NULL, null=True, blank=True)
    truck_plates = models.CharField(verbose_name='Truck Plates', max_length=20, unique=True, blank=True)
    loading_date = models.DateField(verbose_name='Loading Date', default=timezone.now)
    unloading_date = models.DateField(verbose_name='Unloading Date', default=timezone.now)
    info = models.TextField(verbose_name='Additional Information', max_length=2000, default='Transport Additional Information')

    ORDER_STATUS = (
        ('p', 'In produce'),
        ('l', 'Loaded'),
        ('y', 'Delivered'),
        ('d', 'Declined'),
    )

    status = models.CharField(verbose_name='Status', choices=ORDER_STATUS, max_length=1, default='p', blank=True, editable=True)

    MAIL_STATUS = (
        ('n', 'Not Sent'),
        ('s', 'Sent Out'),
    )

    mail = models.CharField(verbose_name='Send Mail', choices=MAIL_STATUS, default='n', max_length=1, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.mail == 's':
            leaders_group = Group.objects.get(name='Leaders')
            leaders_group_emails = leaders_group.user_set.values_list('email', flat=True)

            subject = 'New Transport Order Created'
            message = f'A new order with order number {self.seller_order} has been created and requires your attention.'

            from_email = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, message, from_email, leaders_group_emails)

        order_instance, created = Order.objects.get_or_create(order_nr=self.seller_order.buyer_order.order_nr)
        order_instance.order_status = self.status
        order_instance.transport = self.transport_company
        order_instance.transport_plates = self
        order_instance.transport_load_date = self
        order_instance.transport_unload_date = self
        order_instance.save()

    def __str__(self):
        return str(self.seller_order)

    class Meta:
        verbose_name = 'Transport'
        verbose_name_plural = 'Transports'


class TransportCompany(models.Model):
    name = models.CharField(verbose_name='Company', max_length=1000)
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
        verbose_name = 'TransportCompany'
        verbose_name_plural = 'TransportCompanies'


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
    product_image = models.ImageField(verbose_name='Product Image', upload_to='products', null=True, blank=True)

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
    email = models.EmailField(verbose_name='Email', blank=True)
    tel_number = models.CharField(
        verbose_name="Telephone Number",
        max_length=15,
        blank=True,
        validators=[RegexValidator(regex=r'^\+370\d{8}$',
                                   message="Lithuanian phone number must start with +370 and have 8 additional digits.",
                                   code='invalid_phone_number'
                                   )
                    ]
    )
    user_client = models.OneToOneField(to=User, verbose_name='User Client', on_delete=models.SET_NULL, null=True, blank=True)
    info = models.TextField(verbose_name='Additional Information', max_length=5000, blank=True)

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
    order_nr = models.CharField(verbose_name='Order Number', max_length=10, unique=True, blank=True)
    buyer = models.ForeignKey(to='Buyer', verbose_name='Buyer', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(to='Product',verbose_name='Product',  on_delete=models.SET_NULL, null=True, blank=True)
    buyer_price = models.DecimalField(verbose_name='Buyer Price', max_digits=10, decimal_places=2, default=0.0)
    delivery_date_from = models.DateField(verbose_name='Delivery Date From', default=timezone.now)
    delivery_date_to = models.DateField(verbose_name='Delivery Date To', default=timezone.now)

    ORDER_STATUS = (
        ('a', 'Accepted'),
        ('d', 'Declined'),
    )

    status = models.CharField(verbose_name='Order Status', choices=ORDER_STATUS, default='a', max_length=1, blank=True)

    MAIL_STATUS = (
        ('n', 'Not Sent'),
        ('s', 'Sent Out'),
    )

    mail = models.CharField(verbose_name='Send Mail', choices=MAIL_STATUS, default='n', max_length=1, blank=True)

    def __str__(self):
        return self.order_nr

    def save(self, *args, **kwargs):
        if not self.order_nr:
            used_order_numbers = BuyerOrder.objects.values_list('order_nr', flat=True)
            new_number = 1
            while f'BWS{new_number:04}' in used_order_numbers:
                new_number += 1
            self.order_nr = f'BWS{new_number:04}'

        if self.buyer is not None:
            self.user_client = self.buyer.user_client

        super().save(*args, **kwargs)

        if self.buyer is not None:
            order_instance, created = Order.objects.get_or_create(order_nr=self.order_nr)
            order_instance.buyer_info = self
            order_instance.order_status = self.status
            order_instance.user_client = self.buyer.user_client
            order_instance.save()

        if self.buyer is not None and self.mail == 's':
            sales_managers_group = Group.objects.get(name='Sales managers')
            sales_managers_emails = sales_managers_group.user_set.values_list('email', flat=True)

            subject = 'New Buyer Order Created'
            message = f'A new order with order number {self.order_nr} has been created and requires your attention.'

            from_email = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, message, from_email, sales_managers_emails)

        def delete(self, *args, **kwargs):
            if self.order_nr:
                self.order_nr.delete()
            super(BuyerOrder, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'BuyerOrder'
        verbose_name_plural = 'BuyerOrders'


def delete_order_on_buyer_order_delete(sender, instance, **kwargs):
    try:
        order_instance = Order.objects.get(order_nr=instance.order_nr)
        order_instance.delete()
    except Order.DoesNotExist:
        pass


signals.pre_delete.connect(delete_order_on_buyer_order_delete, sender=BuyerOrder)


class SellerOrder(models.Model):
    buyer_order = models.OneToOneField(to='BuyerOrder', on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(to='Seller', on_delete=models.SET_NULL, null=True, blank=True)
    production_product = models.ForeignKey(to='Product', verbose_name='Production Product', on_delete=models.SET_NULL, null=True, blank=True)
    trailer = models.ForeignKey(to=Trailer, verbose_name='Trailer', on_delete=models.SET_NULL, null=True, blank=True)
    seller_price = models.DecimalField(verbose_name='Seller Price', max_digits=10, decimal_places=2, default=0.0)
    transport_price = models.DecimalField(verbose_name='Transport Price', max_digits=10, decimal_places=2, default=0.0)
    quantity = models.IntegerField(verbose_name='Quantity', default=0)
    total_price = models.DecimalField(verbose_name='Total Price', max_digits=10, decimal_places=2, default=0.0)
    production_date = models.DateField(verbose_name='Production Date', default=timezone.now)

    ORDER_STATUS = (
        ('a', 'Accepted'),
        ('p', 'In produce'),
        ('d', 'Declined'),
    )

    status = models.CharField(verbose_name='Order Status', choices=ORDER_STATUS, default='a', max_length=1, blank=True)

    MAIL_STATUS = (
        ('n', 'Not Sent'),
        ('s', 'Sent Out'),
    )

    mail = models.CharField(verbose_name='Send Mail', choices=MAIL_STATUS, default='n', max_length=1, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.mail == 's':
            transport_managers_group = Group.objects.get(name='Transport managers')
            transport_managers_emails = transport_managers_group.user_set.values_list('email', flat=True)

            subject = 'New Seller Order Created'
            message = f'A new order with order number {self.buyer_order} has been created and requires your attention.'

            from_email = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, message, from_email, transport_managers_emails)

        order_instance, created = Order.objects.get_or_create(order_nr=self.buyer_order.order_nr)
        order_instance.seller_info = self
        order_instance.order_status = self.status
        order_instance.price = self.total_price
        order_instance.production_date = self.production_date
        order_instance.save()

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
    order_nr = models.CharField(verbose_name='Order Number', max_length=20, unique=True, blank=True, editable=False)
    creating_date = models.DateTimeField(verbose_name='Create Date', default=timezone.now, editable=False)
    buyer_info = models.ForeignKey(to='BuyerOrder', verbose_name='Buyer', on_delete=models.CASCADE, null=True, blank=True)
    seller_info = models.ForeignKey(to='SellerOrder', verbose_name='Seller', on_delete=models.CASCADE, null=True, blank=True)
    price = models.CharField(verbose_name='Price', max_length=10, blank=True, editable=False)
    production_date = models.CharField(verbose_name='Production Date', max_length=10, blank=True, editable=False)
    transport = models.ForeignKey(to='TransportCompany', verbose_name='Transport Information', on_delete=models.CASCADE, null=True, blank=True, related_name='orders_as_transport')
    transport_plates = models.ForeignKey(to='Transport', verbose_name='Truck Plates', on_delete=models.CASCADE, null=True, blank=True, related_name='orders_as_plates')
    transport_load_date = models.ForeignKey(to='Transport', verbose_name='Transport Loading Date', on_delete=models.CASCADE, null=True, blank=True, related_name='orders_as_load_date')
    transport_unload_date = models.ForeignKey(to='Transport', verbose_name='Transport Unloading Date', on_delete=models.CASCADE, null=True, blank=True, related_name='orders_as_unload_date')
    user_client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    ORDER_STATUS = (
        ('a', 'Accepted'),
        ('p', 'In produce'),
        ('l', 'Loaded'),
        ('y', 'Delivered'),
        ('d', 'Declined'),
    )

    order_status = models.CharField(verbose_name='Status', choices=ORDER_STATUS, max_length=20, blank=True, editable=False)

    def __str__(self):
        return self.order_nr

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
