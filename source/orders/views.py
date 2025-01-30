from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
import sys

sys.stdout.reconfigure(encoding='utf-8')

def order_create(request):
    if request.method == 'POST':
        print("POST-запрос получен:".encode('utf-8').decode('utf-8'), request.POST)

        table_number = request.POST.get('table_number')
        items = request.POST.getlist('items[]')
        prices = request.POST.getlist('prices[]')
        quantities = request.POST.getlist('quantities[]')

        if not table_number or not items or not prices or not quantities:
            return render(request, 'order_create.html', {'error': 'Заполните все поля.'})

        try:
            print(f"Создание заказа для стола {table_number}")
            order = Order.objects.create(table_number=table_number)
            print(f"Заказ создан: {order.id}")

            for item, price, quantity in zip(items, prices, quantities):
                try:
                    price = float(price)
                    quantity = int(quantity)
                except ValueError:
                    print(f"Ошибка преобразования: price={price}, quantity={quantity}")
                    return render(request, 'order_create.html', {'error': 'Некорректные данные'})

                print(f"Добавление товара: {item}, цена: {price}, количество: {quantity}")
                OrderItem.objects.create(
                    order=order,
                    name=item,
                    price=price,
                    quantity=quantity
                )

            if hasattr(order, 'get_total_price'):
                print("Вызов get_total_price()")
                order.get_total_price()

            print("Редирект на order_list")
            return redirect('order_list')

        except Exception as e:
            print(f"Ошибка при создании заказа: {e}")
            return render(request, 'order_create.html', {'error': f'Ошибка: {e}'})

    return render(request, 'order_create.html')

def order_list(request):
    orders = Order.objects.all()
    query = request.GET.get('q')
    if query:
        orders = orders.filter(table_number__icontains=query) | orders.filter(status__icontains=query)
    return render(request, 'order_list.html', {'orders': orders})

def order_delete(request, id):
    order = get_object_or_404(Order, id=id)
    order.delete()
    return redirect('order_list')

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Order

def order_update(request, id):
    order = get_object_or_404(Order, id=id)

    if request.method == "POST":
        status = request.POST.get('status')

        statuses = [choice[0] for choice in Order.STATUS]
        if status not in statuses:
            return HttpResponse("Некорректный статус", status=400)

        order.status = status
        order.save()

        return redirect('order_list')

    return render(request, 'order_update.html', {'order': order})


def revenue_view(request):
    revenue = Order.calculate_revenue()
    return render(request, 'revenue.html', {'revenue': revenue})

