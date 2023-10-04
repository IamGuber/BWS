from django.shortcuts import render
from django.http import HttpResponse
from .models import  Order


def index(request):
    orders = Order.objects.all()

    context = {
        'orders': orders,
    }

    return render(request, 'index.html', context=context)
