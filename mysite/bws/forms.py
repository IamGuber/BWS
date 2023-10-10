from django import forms
from .models import BuyerOrder, Product, Buyer
from django.contrib.auth.models import User


class ProductFilterForm(forms.Form):
    width = forms.IntegerField(required=False)
    length = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)
    thickness = forms.IntegerField(required=False)


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
