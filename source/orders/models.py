from django.db import models
from django.db.models import Sum

class Order(models.Model):
    STATUS = [
        ('в ожидании', 'В ожидании'),
        ('готово', 'Готово'),
        ('оплачено', 'Оплачено'),
    ]

    table_number = models.IntegerField()
    status = models.CharField(choices=STATUS, max_length=20, default='в ожидании')
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f"Заказ {self.id} - Стол {self.table_number} ({self.status})"

    def update_total_price(self):
        total = self.order_items.aggregate(total=Sum(models.F('price') * models.F('quantity')))['total'] or 0
        self.total_price = total
        self.save()

    @classmethod
    def calculate_revenue(cls):
        return cls.objects.filter(status='оплачено').aggregate(total=Sum('total_price'))['total'] or 0


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()

    def get_total_price(self):
        return self.price * self.quantity
