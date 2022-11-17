from django import forms
from django.utils.translation import ugettext as _

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    quantity = forms.IntegerField(label='', initial=1, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': 1, 'max':10}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)