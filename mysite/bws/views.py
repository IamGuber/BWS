from django.shortcuts import render
from django.http import HttpResponse
from .models import Buyer, Seller


def index(request):
    clients = Buyer.objects.all().count()
    partners = Seller.objects.all().count()

    context = {
        'clients': clients,
        'partners': partners,
    }

    return render(request, 'index.html', context=context)
