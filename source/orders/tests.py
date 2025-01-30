from django.test import TestCase
from orders.models import Order, OrderItem
from decimal import Decimal


class OrderTestCase(TestCase):

    def test_order_creation(self):
        print("Тест создания заказа запущен.")
        order = Order.objects.create(table_number=1)
        self.assertEqual(order.table_number, 1)
        self.assertEqual(order.status, 'в ожидании')
        self.assertEqual(order.total_price, Decimal('0.00'))
        print("Заказ создан.")

    def test_order_item_creation(self):
        order = Order.objects.create(table_number=1)

        order_item = OrderItem.objects.create(order=order, name="Pizza", price=Decimal('10.00'), quantity=2)
        self.assertEqual(order_item.name, "Pizza")
        self.assertEqual(order_item.price, Decimal('10.00'))
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.get_total_price(), Decimal('20.00'))

    def test_update_total_price(self):
        order = Order.objects.create(table_number=1)

        OrderItem.objects.create(order=order, name="Pizza", price=Decimal('10.00'), quantity=2)
        OrderItem.objects.create(order=order, name="Pasta", price=Decimal('5.00'), quantity=1)
        order.update_total_price()
        self.assertEqual(order.total_price, Decimal('25.00'))


    def test_calculate_revenue(self):
        print("Тест расчета выручки запущен.")
        order_1 = Order.objects.create(table_number=1, status='оплачено', total_price=100.00)
        order_2 = Order.objects.create(table_number=2, status='в ожидании', total_price=50.00)
        order_3 = Order.objects.create(table_number=3, status='оплачено', total_price=200.00)

        total_revenue = Order.calculate_revenue()

        print(f"Вычисленная выручка: {total_revenue}")
        self.assertEqual(total_revenue, 300.00)
