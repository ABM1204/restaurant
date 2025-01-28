from django.shortcuts import render, redirect
from .models import Order, OrderItem


def order_create(request):
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        items = request.POST.getlist('items[]')
        prices = request.POST.getlist('price[]')
        quantities = request.POST.getlist('quantity[]')

        if not table_number or not items or not prices or not quantities:
            return render(request, 'order_create.html', {'error': 'Заполните все поля.'})

        try:
            order = Order.objects.create(table_number=table_number)
            for item, price, quantity in zip(items, prices, quantities):
                OrderItem.objects.create(
                    order=order,
                    name=item,
                    price=float(price),
                    quantity=int(quantity)
                )
            order.get_total_price()
            return redirect('order_success')
        except Exception as e:
            return render(request, 'order_create.html', {'error': f'Ошибка: {e}'})

    return render(request, 'order_create.html')


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})
