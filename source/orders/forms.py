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

        try:
            items_list = items.split(',')
            prices_list = [float(price) for price in prices.split(',')]
            quantities_list = [int(quantity) for quantity in quantities.split(',')]
        except ValueError:
            raise forms.ValidationError(
                "Неверный формат данных. Убедитесь, что значения разделены запятыми и являются правильными числами.")

        if len(items_list) != len(prices_list) or len(prices_list) != len(quantities_list):
            raise forms.ValidationError("Количество позиций, цен и количеств не совпадает.")

        for price in prices_list:
            if price <= 0:
                raise forms.ValidationError("Цена должна быть положительным числом.")

        for quantity in quantities_list:
            if quantity <= 0:
                raise forms.ValidationError("Количество должно быть положительным числом.")

        return cleaned_data
