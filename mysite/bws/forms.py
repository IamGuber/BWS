from django import forms
from .models import BuyerOrder, Product, Buyer, SellerOrder
from django.contrib.auth.models import User


class ProductFilterForm(forms.Form):
    width = forms.IntegerField(required=False)
    length = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)
    thickness = forms.IntegerField(required=False)


class SellerOrderForm(forms.ModelForm):
    class Meta:
        model = SellerOrder
        fields = ['production_product']

    def __init__(self, *args, **kwargs):
        super(SellerOrderForm, self).__init__(*args, **kwargs)
        self.fields['production_product'].queryset = Product.objects.filter(name__icontains='n')


class BuyerOrderForm(forms.ModelForm):
    class Meta:
        model = BuyerOrder
        fields = ['product', ]

    def __init__(self, *args, **kwargs):
        super(BuyerOrderForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.exclude(name__icontains='n')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class BuyerUpdateForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['email']
