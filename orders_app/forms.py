from django.forms import ModelForm
from django import forms
from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update(
            {'onchange': 'form.submit();'})
