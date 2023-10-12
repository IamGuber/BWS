from django.shortcuts import render, get_object_or_404
from .models import Order, Product
from .forms import ProductFilterForm, BuyerOrderForm, UserUpdateForm, BuyerUpdateForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import Group


def index(request):
    orders = Order.objects.all()
    product_counts = Product.objects.annotate(order_count=Count('buyerorder'))
    sorted_product_counts = product_counts.order_by('-order_count')
    top_product_counts = sorted_product_counts[:8]

    top_orders = []

    for product_count in top_product_counts:
        product_type = product_count.name
        orders_with_product = orders.filter(buyer_info__product__name=product_type)
        if orders_with_product.exists():
            top_orders.append(orders_with_product.first())

    context = {
        'orders': top_orders,
    }

    return render(request, 'index.html', context=context)


class ProductsListView(generic.ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.exclude(name__contains='n')
        form = ProductFilterForm(self.request.GET)

        if form.is_valid():
            width = form.cleaned_data.get('width')
            length = form.cleaned_data.get('length')
            height = form.cleaned_data.get('height')
            thickness = form.cleaned_data.get('thickness')

            if width:
                queryset = queryset.filter(width__exact=width)
            if length:
                queryset = queryset.filter(length__exact=length)
            if height:
                queryset = queryset.filter(height__exact=height)
            if thickness:
                queryset = queryset.filter(thickness__exact=thickness)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductFilterForm(self.request.GET)
        return context


class ProductDetailView(FormMixin, generic.DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'
    form_class = BuyerOrderForm

    def get_success_url(self):
        return reverse('product', kwargs={'product_id': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.info(request, f"Product {self.object.name} is ordered.")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.product = self.object
        form.instance.buyer = self.request.user.buyer
        form.save()

        purchasing_managers_group = Group.objects.get(name='Purchasing managers')
        purchasing_managers_emails = purchasing_managers_group.user_set.values_list('email', flat=True)

        subject = f'New Order: {self.object.name}'
        message = f'A new order has been placed for the product: {self.object.name}.\n\nOrder details:\n{form.instance}'

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [manager.email for manager in Group.objects.get(name='Purchasing managers').user_set.all()]

        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, purchasing_managers_emails)

        messages.info(self.request, f"Please wait for a manager to contact you.")

        return super().form_valid(form)

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('product_id')
        return get_object_or_404(Product, pk=product_id)


class UserOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    context_object_name = 'user_orders'

    def get_queryset(self):
        queryset = Order.objects.filter(user_client=self.request.user)
        order_number = self.request.GET.get('order_number')
        order_status = self.request.GET.get('order_status')
        delivery_date = self.request.GET.get('delivery_date')
        product_name = self.request.GET.get('product_name')

        if order_number:
            queryset = queryset.filter(order_nr__icontains=order_number)
        if order_status:
            queryset = queryset.filter(order_status=order_status)
        if delivery_date:
            queryset = queryset.filter(transport_unload_date__unloading_date=delivery_date)
        if product_name:
            queryset = queryset.filter(buyer_info__product__name__icontains=product_name)
        return queryset


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"This username: {username}, is taken! Try another one.")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"This {email} is taken! Try another one.")
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password1)
                    messages.info(request, f"User {username} is successfully registered!")
                    return redirect('login')
        else:
            messages.error(request, "Passwords don't match!")
            return redirect('register')
    else:
        return render(request, 'registration/register.html')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        buyer_form = BuyerUpdateForm(request.POST, instance=request.user.buyer)
        if user_form.is_valid() and buyer_form.is_valid():
            request.user.email = user_form.cleaned_data['email']
            user_form.save()
            buyer_form.save()
            messages.success(request, f'Profile updated!')
            return redirect('profile')

    user_form = UserUpdateForm(instance=request.user)
    buyer_form = BuyerUpdateForm(instance=request.user.buyer)

    context = {
        'user_form': user_form,
        'buyer_form': buyer_form,
    }

    return render(request, 'profile.html', context=context)
