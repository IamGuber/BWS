from django import forms


class ProductFilterForm(forms.Form):
    width = forms.IntegerField(required=False)
    length = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)
    thickness = forms.IntegerField(required=False)
