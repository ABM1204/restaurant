from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, DeleteView, UpdateView, TemplateView
from .models import Order, OrderItem


import sys
sys.stdout.reconfigure(encoding='utf-8')

class OrderCreateView(View):
    def get(self, request):
        return render(request, 'order_create.html')

    def post(self, request):
        table_number = request.POST.get('table_number')
        items = request.POST.getlist('items[]')
        prices = request.POST.getlist('prices[]')
        quantities = request.POST.getlist('quantities[]')

        if not table_number or not items or not prices or not quantities:
            return render(request, 'order_create.html', {'error': 'Заполните все поля.'})

        try:
            order = Order.objects.create(table_number=table_number)

            for item, price, quantity in zip(items, prices, quantities):
                try:
                    price = float(price)
                    quantity = int(quantity)

                    if price < 0 or quantity < 0:
                        raise ValueError("Цена и количество должны быть неотрицательными")

                    OrderItem.objects.create(order=order, name=item, price=price, quantity=quantity)
                except ValueError as e:
                    order.delete()
                    return render(request, 'order_create.html', {'error': str(e)})
                except Exception as e:
                    order.delete()
                    return render(request, 'order_create.html', {'error': f'Ошибка создания товара: {e}'})
            order.update_total_price()

            return redirect('order_list')

        except Exception as e:
            return render(request, 'order_create.html', {'error': f'Ошибка создания заказа: {e}'})


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
        return context