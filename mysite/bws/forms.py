from django import forms
from .models import SellerOrder, BuyerOrder, Buyer, Product


class SellerOrderForm(forms.ModelForm):
    buyer_order = forms.ModelChoiceField(queryset=BuyerOrder.objects.all(), label='Select Order Nr.', required=False)
    buyer = forms.ModelChoiceField(queryset=Buyer.objects.all(), label='Buyer', required=False)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Product', required=False)

    class Meta:
        model = SellerOrder
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SellerOrderForm, self).__init__(*args, **kwargs)

        buyer_order = self.instance.buyer_order
        if buyer_order:
            self.fields['buyer'].queryset = Buyer.objects.filter(pk=buyer_order.buyer_id)
            self.fields['product'].queryset = Product.objects.filter(pk=buyer_order.product_id)

            self.initial['buyer'] = buyer_order.buyer
            self.initial['product'] = buyer_order.product

        self.fields['buyer'].widget.attrs['disabled'] = True
        self.fields['product'].widget.attrs['disabled'] = True
