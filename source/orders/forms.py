from django import forms
from .models import Order, OrderItem

class OrderItemForm(forms.Form):
    name = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    quantity = forms.IntegerField(min_value=1)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number']

    items = forms.CharField(widget=forms.HiddenInput(), required=True)
    prices = forms.CharField(widget=forms.HiddenInput(), required=True)
    quantities = forms.CharField(widget=forms.HiddenInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        items = cleaned_data.get("items")
        prices = cleaned_data.get("prices")
        quantities = cleaned_data.get("quantities")

        if not items or not prices or not quantities:
            raise forms.ValidationError("Заполните все поля.")

        return cleaned_data
