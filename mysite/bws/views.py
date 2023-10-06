from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Order, Product
from .forms import ProductFilterForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    orders = Order.objects.all()

    context = {
        'orders': orders,
    }

    return render(request, 'index.html', context=context)


def products(request):
    products = Product.objects.exclude(name__contains='n')
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        width = form.cleaned_data.get('width')
        length = form.cleaned_data.get('length')
        height = form.cleaned_data.get('height')
        thickness = form.cleaned_data.get('thickness')

        if width:
            products = products.filter(width__gte=width)
        if length:
            products = products.filter(length__gte=length)
        if height:
            products = products.filter(height__gte=height)
        if thickness:
            products = products.filter(thickness__gte=thickness)

    context = {
        'products': products,
        'form': form,
    }

    return render(request, 'products.html', context=context)


def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'product.html', context=context)


class UserOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    context_object_name = 'user_orders'

    def get_queryset(self):
        queryset = Order.objects.filter(user_client=self.request.user)
        return queryset
