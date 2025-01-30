import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, DeleteView, UpdateView, TemplateView
from django.db.models import Q
from .forms import OrderForm
from .models import Order, OrderItem

import sys

sys.stdout.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)


class OrderCreateView(View):
    def get(self, request):
        form = OrderForm()
        return render(request, 'order_create.html', {'form': form})

    def post(self, request):
        form = OrderForm(request.POST)
        if not form.is_valid():
            logger.error(f"Form errors: {form.errors}")
            return render(request, 'order_create.html', {'form': form, 'error': 'Заполните все поля корректно.'})

        table_number = form.cleaned_data['table_number']
        items = form.cleaned_data['items'].split(',')
        prices = form.cleaned_data['prices'].split(',')
        quantities = form.cleaned_data['quantities'].split(',')

        try:
            order_items = self._validate_and_prepare_order_items(items, prices, quantities)
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return render(request, 'order_create.html', {'form': form, 'error': str(e)})

        try:
            order = Order.objects.create(table_number=table_number)
            logger.info(f"Order created with id: {order.id}")


            for item in order_items:
                OrderItem.objects.create(
                    order=order,
                    name=item['name'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                logger.info(f"OrderItem created: {item}")

            order.update_total_price()
            logger.info(f"Total price for order {order.id} updated.")


            return redirect('order_list')

        except Exception as e:
            logger.error(f"Error during order creation: {str(e)}")
            return render(request, 'order_create.html', {'form': form, 'error': f'Ошибка создания заказа: {str(e)}'})

    def _validate_and_prepare_order_items(self, items, prices, quantities):
        if not (len(items) == len(prices) == len(quantities)):
            raise ValueError("Количество позиций, цен и количеств не совпадает.")

        order_items = []
        for item, price, quantity in zip(items, prices, quantities):
            try:
                price = float(price)
                quantity = int(quantity)
                if price <= 0 or quantity <= 0:
                    raise ValueError("Цена и количество должны быть положительными числами.")

                order_items.append({'name': item, 'price': price, 'quantity': quantity})

            except ValueError:
                raise ValueError(f"Ошибка в данных товара: {item}. Убедитесь, что цена и количество корректны.")

        return order_items


from django.db.models import Q


def order_list(request):
    orders = Order.objects.all()
    query = request.GET.get('q')
    if query:
        if query.isdigit():
            orders = orders.filter(table_number=query)
        else:
            query_lower = query.lower()
            orders = orders.filter(status__iexact=query_lower)

    return render(request, 'order_list.html', {'orders': orders})


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order_delete.html'
    context_object_name = 'order'
    success_url = reverse_lazy('order_list')

    def get_object(self, queryset=None):
        return Order.objects.get(id=self.kwargs['id'])


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'order_update.html'
    fields = ['status']
    context_object_name = 'order'

    def get_object(self, queryset=None):
        return Order.objects.get(id=self.kwargs['id'])

    def get_success_url(self):
        return reverse_lazy('order_list')


class RevenueView(TemplateView):
    template_name = 'revenue.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['revenue'] = Order.calculate_revenue()
        context['orders'] = Order.objects.filter(status='оплачено')
        return context
