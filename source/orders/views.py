from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, DeleteView, UpdateView, TemplateView

from .forms import OrderForm
from .models import Order, OrderItem

import sys

sys.stdout.reconfigure(encoding='utf-8')


class OrderCreateView(View):
    def get(self, request):
        form = OrderForm()
        return render(request, 'order_create.html', {'form': form})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            table_number = form.cleaned_data['table_number']
            items = form.cleaned_data['items'].split(',')
            prices = form.cleaned_data['prices'].split(',')
            quantities = form.cleaned_data['quantities'].split(',')

            try:
                order = Order.objects.create(table_number=table_number)

                for item, price, quantity in zip(items, prices, quantities):
                    try:
                        price = float(price)
                        quantity = int(quantity)

                        if price <= 0 or quantity <= 0:
                            raise ValueError("Цена и количество должны быть положительными")

                        OrderItem.objects.create(order=order, name=item, price=price, quantity=quantity)

                    except ValueError as e:
                        order.delete()
                        return render(request, 'order_create.html', {'form': form, 'error': str(e)})

                    except Exception as e:
                        order.delete()
                        return render(request, 'order_create.html', {'form': form, 'error': f'Ошибка создания товара: {e}'})

                order.update_total_price()

                return redirect('order_list')

            except Exception as e:
                return render(request, 'order_create.html', {'form': form, 'error': f'Ошибка создания заказа: {e}'})
        else:
            return render(request, 'order_create.html', {'form': form, 'error': 'Заполните все поля корректно.'})


def order_list(request):
    orders = Order.objects.all()
    query = request.GET.get('q')
    if query:
        orders = orders.filter(table_number__icontains=query) | orders.filter(status__icontains=query)
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
